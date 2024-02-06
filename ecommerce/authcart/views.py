from tokenize import generate_tokens
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
# from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.views.decorators.csrf import csrf_protect

@csrf_protect


# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request,"Password incorrect")
            return render(request, 'signup.html')

        # Check if the user already exists
        elif User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.info(request, "User already exists")
            return render(request, 'signup.html')

        # Create a new user
        else:
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()
            
            email_subject = 'Activate your blog account.'
            message = render_to_string('activate.html', {
                'user': user,
                'domain': '127.0.0.1',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email_message= EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,[email],)
            email_message.send()
            messages.success(request, f"Activate Your Account by clicking the link in Your Gmail")
            return redirect('/auth/login/')

    else:  
        # Display the empty form
        return render(request, 'signup.html')
    
class ActivateAccountView(View):
    def get(self,request,uidb64, token):
        try:
            uid= force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as identifer:
            user= None
        if user is not None and generate_tokens.check_token(user,token):
            user.is_active= False
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login')
        return redirect(request,'/activatefail.html' ) 


    # def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('login')  # Assuming you have a named URL for login

        return redirect('/activatefail.html')  # Assuming you have a named URL for activatefail
    
def handellogin(request):
    if request.method == "POST":
        username = request.POST['username']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            if myuser.is_active:
                login(request, myuser)
                messages.success(request, "Login Success")
                return redirect('/')
            else:
                messages.error(request, "Account not activated. Check your email for activation instructions.")
        else:
            messages.error(request, "Invalid Credentials")
        
    return render(request, 'login.html')

def handellogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login')



















# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['pass1']
#         confirm_password = request.POST['pass2']

#         if password != confirm_password:
#             messages.warning(request, "Password incorrect")
#             return render(request,'signup.html')

#         # Check if the user already exists
#         elif User.objects.filter(Q(email=email) | Q(username=username)).exists():
#             messages.info(request, "User already exists")

#         # Create a new user
#         else:
#             user = User.objects.create_user(username, email, password)
#             user.is_active = False
#             user.save()
            
#             email_subject = 'Activate your blog account.'
#             message = render_to_string('activate.html', {
#                 'user': user,
#                 'domain': 'http://127.0.0.1',
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             email_message= EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,[email],)
#             email_message.send()
#             messages.success(request, f"Activate Your Account by clicking the link in Your Gmail{message}")
#             return redirect('/login/')
#         return render(request, 'signup.html')
#     else:  
#         # Display the empty form
#         return render(request, 'signup.html')
    
# class ActivateAccountView(View):
    def get(self,request,uidb64, token):
        try:
            uid= force_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(pk=uid)
        except Exception as identifer:
            user= None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active= True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/login')
        return redirect('/activatefail.html' )        
    
   # Create your views here.
# class SignupView(View):
    def get(self, request):
        # Display the empty form
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Password incorrect")
            return render(request, 'signup.html')

        # Check if the user already exists
        elif User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.info(request, "User already exists")

        # Create a new user
        else:
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            # Send activation email
            self.send_activation_email(request, user)

            messages.success(request, "Activate Your Account by clicking the link in Your Gmail")
            return redirect('login')  # Assuming you have a named URL for login

        return render(request, 'signup.html')

    def send_activation_email(self, request, user):
        email_subject = 'Activate your blog account.'
        message = render_to_string('activate.html', {
            'user': user,
            'domain': request.build_absolute_uri('/')[:-1],  # Use the domain from the request
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [user.email])
        email_message.send()

    


