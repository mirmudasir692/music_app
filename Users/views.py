from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from Users.models import CustomUser
import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.conf import settings
# Create your views here.


class LoginUserView(View):
    template_name = 'music/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request, 'please enter the right credentials')
            return redirect('users:login')
        login(request, user)
        return redirect('music:home')


def logout_user(request):
    logout(request)
    return redirect('music:home')


class CreateUserView(View):
    template_name = 'music/createuser.html'

    def get(self, request):
        return render(request, self.template_name)

    def check_age(self, dob):
        dob_string = dob.split('-')[0]
        current_year = datetime.date.today().year
        audult_ness = int(current_year)-int(dob_string)
        if audult_ness >= 18:
            return True
        else:
            False

    def generate_otp(length=6):
        otp = ''.join(random.choice('0123456789') for _ in range(length))
        return otp

    def send_email_to_user(self, email):
        subject = 'You confirmation Otp'
        otp = self.generate_otp()
        message = f"Your OTP is : {otp}"
        recipient_email = email
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_email)
        return otp

    def check_confirmation(self, otp, user_email):
        otp_sent = self.send_email_to_user(user_email)
        if otp == otp_sent:
            return True
        else:
            return False

    def post(self, request):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            adult = self.check_age(dob)
            otp = request.POST.get('otp')
            if adult:

                user = authenticate(email=email, password=password2)
                if user is None:
                    user = CustomUser.objects.create_user(username=username,
                                                          email=email, password=password2, phone=phone, dob=dob, gender=gender)
                    user.save()
                    login(request, user)
                    return redirect('music:home')
                else:
                    messages.warning(request, 'user already exists')
                    return redirect("users:create")
            else:
                messages.warning(request, 'You are not eligible to register')
                return redirect("users:create")


@login_required
def user_profile(request):
    return render(request, 'music/profile.html')


class UpdateUser(View):
    def get(self, request):
        return render(request, 'music/edit_profile.html')

    def post(self, request):
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        user = CustomUser.objects.get(id=user.id)
        user.username = username
        user.email = email
        user.phone = phone
        user.dob = dob
        user.gender = gender
        user.save()
        messages.success(request, 'Successfully updated')
        return redirect('users:update')


class DeleteAccountView(View):
    def get(self, request):
        return render(request, 'music/delete.html')

    def post(self, request):
        user = request.user
        user = CustomUser.objects.get(id=user.id)
        user.delete()
        return redirect('music:home')
