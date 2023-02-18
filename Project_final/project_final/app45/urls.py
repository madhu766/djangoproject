from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
app_name = 'app45'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_attempt, name='register'),
    path('accounts/login/', views.login_attempt, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('token/', views.token_send, name='token_send'),
    path('success/', views.success, name='success'),
    path('verify/<auth_token>/', views.verify, name='verify'),
    path('error/', views.error_page, name='error'),
    path('details/', views.DetailView.as_view(), name='details'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app45/password_reset.html',
         form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='app45/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app45/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app45/password_reset_complete.html'), name='password_reset_complete'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app45/passwordchange.html',
         form_class=MyPasswordChangeForm), name='password_change'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app45/passwordchangedone.html')),
    path('contact/',views.contact,name='contact'),
    path('success_page/',views.Success,name='success_page')
]
