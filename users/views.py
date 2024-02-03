from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from users.models import User
from django.views.generic import CreateView, TemplateView, UpdateView, View
from users.forms import UserRegisterForm, UserProfileForm, ResetPasswordForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from users.services import AppTokenGenerator, send_email_by_django


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = AppTokenGenerator().make_token(user)
            link = f'http://127.0.0.1:8000/activate/{uid}/{token}'
            send_email_by_django('Активация пользователя', f'Для активации пользователя перейдети по ссылке {link}', [user.email,])
        return super().form_valid(form)


class UserChangePasswordView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')


class UserChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    success_url = reverse_lazy('users:password_change_done')


class RecoveryView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'users/password_reset.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                print(user.email)
                new_password = '!qwert1234'
                user.set_password(new_password)
                user.save()
                send_email_by_django('Сброс пароля', f'Установлен новый пароль: {new_password}.',
                                     [user.email, ])
                return redirect('users:reset_done')
        return render(request, 'users/password_reset.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not AppTokenGenerator().check_token(user, token):
                return redirect('users:activated')
            if user.is_active:
                return redirect('users:activated')
            user.is_active = True
            user.save()
            return redirect('users:activated')
        except Exception as ex:
            pass
        return redirect('users:login')


class ActivatedView(TemplateView):
    template_name = 'activated.html'

class ResetDoneView(TemplateView):
    template_name = 'reset_done.html'