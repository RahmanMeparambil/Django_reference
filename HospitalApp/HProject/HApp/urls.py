from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name ='home'),
    path('about',views.about,name='about'),
    path('login',views.Vlogin,name='login'),
    path('signup',views.signup,name='signup'),
    path('bookappointment',views.BookAppointment,name='bookappointment'),
    path('activate/<uidb64>/<token>',views.activate ,name ='activate'),
    path('activate_appointment/<uidb64>/<token>',views.Vactivate_appointment,name='activate_appointment'),
    path('patienthome',views.patient_home,name='patient_home'),
    path('admin_home',views.admin_home,name = 'admin_home'),
    path('appointment',views.appointment,name='appointment'),
    path('getloan',views.get_loan,name='getloan'),
    path('signout',views.signout,name='signout'),
    path('edit_slot/<id>',views.edit_slot,name='edit_slot'),
    path('delete_slot/<id>',views.delete_slot,name='delete_slot'),
    path('create_slot',views.create_slot,name='create_slot'),
    path('admin',views.admin_home,name ='admin'),
    path('doctors',views.doctors,name='doctors'),
    path('slots',views.create_slot,name='slots'),
    path('reciept',views.reciept,name='reciept'),
    path('add_doctor',views.add_doctor,name='add_doctor'),
    path('add_specialization',views.add_specialization,name='add_specialization'),
    path('add_appointment',views.add_appointment,name= 'add_appointment'),
    path('add_reciept',views.add_reciept,name='add_reciept'),
    path('verify/<uidb64>',views.verify,name='verify'),
    path('password_reset',views.password_reset,name='password_reset'),
    path('doctor_home',views.doctor_home,name = 'doctor_home'),
    path('view_specialization/<spec_id>',views.view_specialization,name='view_specialization'),
    path('view_doctor/<doc_id>',views.ViewDoctor,name='view_doctor'),
    path('messages',views.msg,name='messages'),
    path('search',views.search,name='search'),
    path('view_message/<id>',views.view_message,name="view_message"),
    path('add_message/<id>',views.add_message,name='add_message'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
