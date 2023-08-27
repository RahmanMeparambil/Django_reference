from django.shortcuts import render
from django.http import HttpResponse
from .form import AddRegisterForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    if request.method == 'POST':
        form  = AddRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            # ---- Composing
            from_email = settings.EMAIL_HOST_USER
            to_email = [form['email'].value(),'email',]
            subject = "Registration Completed - Django Registration"
            message = render_to_string("Email.html",
            {
                'name':form['name'].value(),
                'address':form['address'].value(),
                'phone':form['phone'].value(),
                'email':form['email'].value(),
                'pincode':form['pincode'].value(),

            })
            email = EmailMessage(subject,message,from_email,to_email)
            email.fail_silenty = True
            if 'file' in request.FILES:
                file = request.FILES['file']

                email.attach(file.name, file.read(), file.content_type)
        
            email.send()
        
            return HttpResponse("Email sent successfully!")
    else:
       form = AddRegisterForm()
    return render(request,'register.html',{
        'form':form
    })