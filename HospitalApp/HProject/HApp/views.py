from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from . tokens import GenerateToken
from django.contrib.auth import login,logout
from .models import *
from django.contrib.auth.hashers import make_password
import random
import datetime
from django.db.models import Q



# CONSTANTS
MAX_APPO = 10
MAX_APPO_PER_SLOT = 3
LIMIT = 1


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'admin.html')
        elif request.user.is_staff:
            return render(request,'doctors_home.html')
        return render(request,'patient_home.html')
    all_spec = Specialization.objects.all()
    all_doc = Doctor.objects.filter(Class='Senior')
    return render(request,'home.html',{'spec':all_spec,'doc':all_doc}) 


def about(request):
    return render(request,'about.html')


def view_specialization(request,spec_id):
    spec = Specialization.objects.get(id=spec_id)
    return render(request,'view_specialization.html',{'spec':spec})


def ViewDoctor(request,doc_id):
    doc = Doctor.objects.get(id=doc_id)
    slot = Slot.objects.filter(Doctor_reg = doc)
    today = datetime.datetime.now().date()
    slots_to = Slot.objects.filter(Doctor_reg = doc,Date__lt=today)
    slots_to.delete()
    return render(request,'view_doctor.html',{'doc':doc , 'slots':slot})


def BookAppointment(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        today = datetime.datetime.now().date()
        all_appo = Appointment.objects.filter(Patient_email=email).count()

        if all_appo > MAX_APPO : 
            messages.info(request,"you have reached the maximum number of appointments")
            return redirect('home')
    
        else:
            try:
                doc = request.POST['doctor']
                spec = request.POST['specialization']
                spec_to_doc = Specialization.objects.get(Specialization_name = spec)
                doc = Doctor.objects.get(Name = doc,Specialization = spec_to_doc)
                slot_id = request.POST['time']

                if slot_id == 'Empty':
                    messages.info(request,'No slots available !')
                    return redirect('home')
                else :
                    slot = Slot.objects.get(id = slot_id)
                    appo_date_str = slot.Date.strftime("%Y-%m-%d")
                    appo_date = datetime.datetime.strptime(appo_date_str, "%Y-%m-%d").date()
                    start_time = slot.Start_time
                    end_time = slot.End_time


            except:
                spec = request.POST['specialization']
                spec_to_doc = Specialization.objects.get(Specialization_name = spec)
                doc = Doctor.objects.filter(Specialization = spec_to_doc,Class = 'Junior')
                if doc.count() == 0:
                    messages.error(request,"No doctors available !")
                    return redirect("home")
                else:
                    appo_date_str = request.POST['date']
                    appo_date = datetime.datetime.strptime(appo_date_str, "%Y-%m-%d").date()
                    minn = float('inf')
                    for d in doc :
                        if Appointment.objects.filter(Doctor_reg = d).count() < minn :
                            doc = d
                slot = request.POST['time'].split(',')
                start_time = slot[0]
                end_time = slot[1]
                ap_count = Appointment.objects.filter(Appointment_date = appo_date,Start_time = slot[0]).count()
                
                if ap_count > MAX_APPO_PER_SLOT : # -----  distributing the patients
                    messages.error(request,f'{slot[0]}-{slot[1]} is Full !')
                    return redirect('home')
            
            if appo_date < today :
                messages.error(request,"Give a valid date")
                return redirect('home')
            elif Appointment.objects.filter(Patient_name=name ,Patient_email=email,Appointment_date = appo_date).count() >0 :
                messages.error(request,"You have already taken an appointment !")
                return redirect('home')

            
            a = Appointment()
            a.Patient_name = name
            a.Doctor_reg = doc
            a.Appointment_date = appo_date
            a.Start_time = start_time
            a.End_time = end_time
            a.Patient_email = email
            a.Specialization = spec
            a.save() 


        a = Appointment.objects.get(Patient_name=name ,Patient_email=email,Appointment_date = appo_date)

        # --Composing
        current_site = get_current_site(request)
        from_email = settings.EMAIL_HOST_USER
        to_email = [email,]
        subject = "Confirm your email @ Medcare - Django Appointment Booking"
        message = render_to_string("AppointmentVerification.html",
            {
                'user':name,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(a.pk)),
                'token':GenerateToken.make_token(a)     
            })
        email = EmailMessage(subject,message,from_email,to_email)
        email.fail_silenty = True
        email.send()

        messages.success(request,'Confirmation email has been sent to your email address !')
        return redirect('home')

    else:
        return render(request,'home.html')
      

def doctor_home(request):
    return render(request,'doctors_home.html')


def Vlogin(request):
    if request.method =='POST':
        username = request.POST['user_name']
        pword = request.POST['pword']
        user = authenticate(username = username,password = pword)
        if user is None:
            messages.error(request,'Bad Credentials')
            return render(request, 'login1.html')
        login(request, user)
        request.session['logg'] = user.id
        if user.is_superuser:
            return redirect('admin_home')
        elif user.is_staff:
            return redirect('doctor_home')
        return redirect('patient_home')
    return render(request,'login1.html')


def patient_home(request):
    return render(request,'patient_home.html')


def admin_home(request):
    return render(request,'admin.html')


def add_doctor(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        spec = request.POST['specialization']
        cls = request.POST['class']
        specialization = Specialization.objects.get(Specialization_name = spec)
        p = ['a','b','c','d','1','2','3','4']
        random.shuffle(p)
        pword = ''.join(p).replace(' ','').replace('.','')
        if User.objects.filter(username = name).count() > 0 :
            messages.error(request,'Already exists')
            return redirect('home')
        d = Doctor.objects.create(Name=name)


        try:
            photo = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            d.Name = name
            d.Specialization = specialization
            d.Image = photo
            d.Email = email
            d.Class = cls
            d.save()


        except:
            d.Name = name
            d.Specialization = specialization
            d.Email = email
            d.Class = cls
            d.save()
        
        user = User.objects.create_user(username=name,email = email,password = pword)
        user.save()

   

        # ---- Composing
        subject = 'Your Account has been Created'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        context = {'domain':get_current_site(request),'username': user.username, 'email': user.email,'uid':urlsafe_base64_encode(force_bytes(user.pk))}
        html_message = render_to_string('account_created.html', context)

        email = EmailMessage(subject, html_message, from_email, recipient_list)
        email.send()

        messages.success(request, 'Doctor Added !')
        return render(request,'add_doctor.html')
    spec = Specialization.objects.all()
    return render(request,'add_doctor.html',{'spec':spec})


def add_specialization(request):
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['description']
        icon = request.POST['icon']
        photo = request.FILES['imgg1']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        s = Specialization()
        s.Specialization_name = name
        s.Description = desc
        s.Icon = icon
        s.Image = photo
        s.save()
    return render(request,'add_specialization.html') 


def verify(request,uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user!=None:
        user.is_staff = True
        user.save()
        request.session['id'] = uid
        return render(request,'password_reset.html')
    else:
        return render(request,'reset_failed.html')


def password_reset(request):
    if request.method == 'POST' :
        p1 = request.POST['pass1']
        p2 = request.POST['pass2']
        if p1 == p2 :
            user = User.objects.get(id = request.session['id'])
            user.password = make_password(p1)
            user.save()
            return render(request,'reset_done.html')
        else:
            messages.error(request,'Passwords are not matching')
            
    return render(request,'password_reset.html')


def get_loan(request):
    return render(request,'get_loan.html')


def doctors(request):
    docs = Doctor.objects.all()
    return render(request,'doctors.html',{'docs':docs})


def doctor_page(request):
    pass


def edit_slot(request, id):
    slot = Slot.objects.get(id = id)
    if request.method == 'POST':
        slot.Date = request.POST['date']
        slot.Start_time = request.POST['start_time']
        slot.End_time = request.POST['end_time']
        slot.save()
        messages.success(request, 'Slot edited successfully')
        return redirect('create_slot')
    return render(request,'edit_slot.html',{'s':slot})


def delete_slot(request, id):
    id = str(id)
    ftf = Slot.objects.get(id=id)
    Slot.objects.filter(id=id).delete()
    messages.success(request, 'Slot deleted successfully')
    return redirect('create_slot')



def create_slot(request):
    user = User.objects.get(id = request.session['logg'])
    doc = Doctor.objects.get(Name = user.username)
    today = datetime.datetime.now().date()
    slots_to = Slot.objects.filter(Doctor_reg = doc,Date__lt=today)
    slots_to.delete()


    if request.method == 'POST': 
        s = Slot()
        s.Doctor_reg = doc
        s.Date = request.POST['date']
        s.Start_time = request.POST['start_time']
        s.End_time = request.POST['end_time']
        s.save()

    slots = Slot.objects.filter(Doctor_reg = doc)
    return render(request,'slot_booking.html',{'s':slots})


def appointment(request):
    if request.user.is_superuser:
        ap = Appointment.objects.all()
    elif request.user.is_staff:
        user = User.objects.get(id = request.session['logg'])
        doc = Doctor.objects.get(Name = user.username)
        ap = Appointment.objects.filter(Doctor_reg = doc)
    else:
        user = User.objects.get(id = request.session['logg'])
        ap = Appointment.objects.filter(Patient_email=user.email)
    return render(request,'appointment.html',{'appointment':ap})


def add_appointment(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        doc_id = request.POST['doctor']
        date = request.POST['date']
        time = request.POST['time'].split(',')
        doc = Doctor.objects.get(id = doc_id)
        spec = doc.Specialization.Specialization_name
        
        a = Appointment()# ------------insert
        a.Appointment_date = date
        a.Patient_name = name
        a.Patient_email = email 
        a.Specialization = spec
        a.Start_time = time[0]
        a.End_time = time[1]
        a.Status = True
        a.Doctor_reg = doc
        a.save()
        messages.info(request,'Appointment added !')
    docs = Doctor.objects.filter(Class='Junior')
    return render(request,'add_appointment.html',{'docs':docs})



def signup(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        fullname = request.POST['full_name']
        email = request.POST['email']
        pword = request.POST['pword']

        if len(username) > 10:
            messages.error(request,f'user name must be under 10 characters ')
            return render(request,'signup.html')
        
        if not username.isalnum():
            messages.error(request,'user name must be Alpha-Numeric')
            return render(request,'signup.html')

        if len(pword) < 8 :
            messages.error(request,'Password is too short')
            return render(request,'signup.html')
        
        if User.objects.filter(username = username) :
             messages.error(request,"username/email is already taken")
             return render(request,'signup.html')
        
        # try:
        # ---- Composing
        subject = "Welcome to Medcare - Django login"
        message = "Hello " + fullname + "!! \n" + "Welcome to Medcare !! \n Thankyou for visiting our website \n we have also sent you a confirmation email , please confirm your email address in order to activate your account. \n\n Thanking You "+fullname
        from_email = settings.EMAIL_HOST_USER
        to_email = [email,]

        send_mail(subject,message,from_email,to_email,fail_silently=True)

        user = User.objects.create_user(username=username,email=email,password=pword)
        user.full_name = fullname
        user.is_active = False
        user.save()
            
        current_site = get_current_site(request)
        subject = "Confirm your email @ Medcare - Django login"
        message = render_to_string("email_confirmation.html",{
                'name':user.full_name,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':GenerateToken.make_token(user)     
            })
        from_email = settings.EMAIL_HOST_USER
        to_email = [email,]

        email = EmailMessage(subject,message,from_email,to_email)
        email.fail_silenty = True
        email.send()

        messages.info(request,"Your account has been successfully created")

    return render(request,'signup.html')
     

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk = uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and GenerateToken.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        return render(request,'activation_succesful.html')
    else:
        return render(request,'activation_failed.html')


def Vactivate_appointment(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        a = Appointment.objects.get(pk = uid)
    except (TypeError,ValueError,OverflowError):
        a = None

    if a is not None and GenerateToken.check_token(a,token):  
        a.Status = True
        a.save()
        # --Composing
        current_site = get_current_site(request)
        from_email = settings.EMAIL_HOST_USER
        to_email = [a.Patient_email,]
        subject = f"Appointment Confirmation - {datetime.datetime.now().date()}"
        message = render_to_string("Appointment_details.html",
            {
                'datetime':a.Appointment_date,
                'name':a.Patient_name,
                'doctor':a.Doctor_reg.Name,
                'specialization':a.Specialization,
                'slot':f'{a.Start_time}-{a.End_time}',
                'id':a.pk,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(a.pk)),
                'token':GenerateToken.make_token(a)     
            })
        email = EmailMessage(subject,message,from_email,to_email)
        email.fail_silenty = True
        email.send()  
        return render(request,'activation_succesful.html')
    else:
        return render(request,'activation_failed.html')


def reciept(request):
    rec = Receipt.objects.all()
    return render(request,'reciept.html',{'rec':rec})


def edit_receipt(request, id):
    slot = Slot.objects.get(id = id)
    if request.method == 'POST':
        slot.Date = request.POST['date']
        slot.Start_time = request.POST['start_time']
        slot.End_time = request.POST['end_time']
        slot.save()
        messages.success(request, 'Receipt edited successfully')
        return redirect('create_slot')
    return render(request,'edit_receipt.html',{'s':slot})


def delete_receipt(request, id):
    id = str(id)
    ftf = Slot.objects.get(id=id)
    Slot.objects.filter(id=id).delete()
    messages.success(request, 'Receipt deleted successfully')
    return redirect('create_receipt')


def add_reciept(request):
    if request.method == 'POST':
        ap_id = request.POST['appointment']
        if ap_id == 'Empty':
            messages.info(request,'No Appointments !')
            return render(request,'add_receipt.html')
        a = Appointment.objects.get(id = ap_id)
        doc = a.Doctor_reg
        patient = a.Patient_name
        email = a.Patient_email
        totalAmount = request.POST['amount']
        if totalAmount.isnumeric():
            totalAmount = float(totalAmount)
        else:
            messages.error(request,'Invalid Amount')
            return render(request,'add_reciept.html',{'ap':a})

        r = Receipt()
        r.Name = patient
        r.Doctor_reg = doc
        r.Email = email
        r.Amount = totalAmount
        r.save()

        Appointment.objects.get(id = ap_id).delete()
        

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    a = Appointment.objects.filter(Status=True,Appointment_date = today)
    return render(request,'add_reciept.html',{'ap':a})


def msg(request):
    current_usr = User.objects.get(id=request.session['logg'])

    msg_count = Message.objects.all().count()#  ---------- replacement for search
    if msg_count == 0:
        users = User.objects.filter(is_staff = True)
        for u in users:
            m = Message()
            m.Sender = u
            m.Recipient = current_usr
            m.Content = 'hello'
            m.save()
 
    sorted_msgs = Message.objects.filter(Recipient=current_usr).order_by('-Timestamp')
    distinct_senders = sorted_msgs.values('Sender__username').distinct()
    sender_usernames = [item['Sender__username'] for item in distinct_senders]
    senders = User.objects.filter(username__in=sender_usernames)

    user_msg_data = []
    for u in senders:
        unread_count = Message.objects.filter(Sender=u,Recipient=current_usr,Is_read=False).count()
        last_message = Message.objects.filter(Sender=u, Recipient=current_usr).order_by('-Timestamp').first()
        user_msg_data.append({
                'user': u,
                'unread_count': unread_count,
                'last_message': last_message
                 })
    context = {
        'user_msg_data': user_msg_data,
        }
    return render(request, 'message_page.html', context)


def view_message(request,id):
    current_user = User.objects.get(id=request.session['logg'])
    user = User.objects.get(id=id)
    msg = Message.objects.filter(Q(Sender=user, Recipient=current_user) | Q(Sender=current_user, Recipient=user)).order_by('Timestamp') 
    unread_msg = msg.filter(Is_read=False)
    for m in unread_msg:
        m.Is_read=True
        m.save()
    return render(request,'view_msg.html',{'msg':msg,'recipient':id,'sender':request.session['logg']})


def add_message(request,id):
    if request.method == 'post':
        sender = request.POST['sender']
        s = User.objects.get(id =sender)
        recipient = request.POST['recipient']
        r = User.objects.get(id=recipient)
        m = Message()
        m.Recipient = r
        m.Sender = s
        m.save() 
    u = User.objects.get(id= id)
    return redirect('view_message',id =u.id)


def search(request):
    q = request.GET['query']
    if q:
        usrs = User.objects.filter(is_staff=True)
        res = usrs.filter(username = q) 
    else:
        res = User.objects.none()
        
    context = {
        'query': q,
        'results': res,
    }
    return render(request, 'search_results.html', context)


def signout(request):
    logout(request)
    return redirect('home')

