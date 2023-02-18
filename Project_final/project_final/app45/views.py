from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . models import Student,Profile
from . forms import StudentRegistrationForm,StudentDetailsForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.

def index(request):
    return render(request,'app45/index.html')

def user_logout(request):
    logout(request)
    return redirect('app45:login')

 
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is taken.')
                return redirect("/register")
            
            user_obj = User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')
        
        except Exception as e:
            print(e)
    return render(request,'app45/register.html')


def send_mail_after_registration(email,token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.01:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )
    

def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def success(request):
    return render(request,'app45/success.html')

def token_send(request):
    return render(request,'app45/token_send.html')

def error_page(request):
    return render(request,'app45/error.html')


def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request,'user not found.')
            return redirect('/accounts/login/')
        
        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request,'Profile is not verified check your email.')
            return redirect('/accounts/login/')
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'wrong password.')
            return redirect('/acccounts/login/')
        
        login(request, user)
        return redirect('/')
    
    return render(request, 'app45/login.html')


class DetailView(View):
          def get(self,request):
                form=StudentDetailsForm()
                return render(request,'app45/details.html',{'form':form})
          def post (self,request):
                form=StudentDetailsForm(request.POST)
                if form.is_valid():
                    user=request.user
                    first_name=form.cleaned_data['first_name']
                    last_name=form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    reg=Student(user=user,first_name=first_name,last_name=last_name,email=email,phone=phone)
                    reg.save()
                    messages.success(request,'Congratulations ! Profile updated successfully')
                    return redirect('/')
                return render(request,'app45/details.html',{'form':form,'active':'btn-primary'})

def contact(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
      

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exist')
            return redirect("app45:contact")

        else:
            user = User.objects.create_user(
                username=username,email=email)
            mydict = {'username': username}
            user.save()
            html_template = 'app45/contact_template.html'
            html_message = render_to_string(html_template,context=mydict)
            subject = 'Welcome to levelup'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject,html_message,email_from,recipient_list)
            message.content_subtype = 'html'
            message.send()
            return redirect("app45:success_page")
    else:
        return render(request, 'app45/contact.html')

def Success(request):
    return render(request,'app45/success_page.html')


            