from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from blog.models import Category
from .forms import SignUpForm
from .models import Profile


class UserRegistrationView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context

    def post(self, request, *args, **kwargs):
        try:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password1 != password2:
                messages.success(request, 'Ikkala parol maydonidagi parollar bir xil emas!!!')
                return redirect('register')

            if User.objects.filter(username=username).first():
                messages.success(request, "Bunday foydalanuvchi avvalroq ro'yxatdan o'tgan!!!")
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.success(request, "Bu email avvalroq ro'yxatdan o'tgan!!!")
                return redirect('register')

            user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user_obj.set_password(raw_password=password1)
            user_obj.save()

            token = str(uuid4())
            profile_obj = Profile.objects.create(user=user_obj, token=token)
            profile_obj.save()
            send_mail_registration(email=email, token=token)
            return redirect('token_send')
        except Exception as e:
            messages.error(request, f"Xatolik {e}")
            return redirect('register')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request=request, message="Foydalanuvchi topilmadi!!!")
            return redirect('login')
        profile = Profile.objects.filter(user=user_obj).first()
        if not profile.is_verified:
            messages.success(request=request, message="Profil tasdiqlanmagan, elektron pochtangizni tekshiring!!!")
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request=request, message="Noto'g'ri parol kiritilgan")
            return redirect('login')
        login(request=request, user=user)
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return redirect('home')

    def get_context_data(self, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['categorys'] = cat_menu
        context['category_count'] = cat_menu.count()
        return context


def send_mail_registration(email: str, token: str):
    subject = "Ro'yxatdan o'tish uchun link"
    message = "Assalomu Alaykum Hurmatli foydalanuvchi!!!\n" \
              f"Ro'yxatdan o'tishni tasdiqlash uchun ushbu http://bultakov.uz/users/verify/{token} havolaga o'ting"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, recipient_list=recipient_list, from_email=from_email)


def success(request):
    return render(request, 'registration/success.html')


def token_send(request):
    return render(request, 'registration/token_send.html')


def verify(request, token: str):
    try:
        profile_obj = Profile.objects.filter(token=token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Sizning hisobingiz allaqachon tasdiqlangan!!!')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Sizning hisobingiz tasdiqlandi!!!')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        messages.success(request, f'Xatolik {e}')
        return redirect('home')


def error_page(request):
    return render(request, 'registration/error.html')
