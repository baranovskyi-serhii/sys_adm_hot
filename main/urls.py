from django.urls import path
from . import views

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('profile.html', views.view_profile, name='profile'),
    path('login.html', views.view_login, name='login'),
    path('logout.html', views.view_logout, name='logout'),
    path('create-account.html', views.view_create_account, name='create_account'),
    path('forgot-password.html', views.view_forgot_password, name='forgot_password'),
    
    # Строрінка після надсилання електронного листа з інструкціями щодо скидання пароля
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # Підтвердження скидання пароля
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сторінка після успішного скидання пароля
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Зміна пароля
    path('profile/change-password/', PasswordChangeView.as_view(), name='password_change'),
    # Сторінка після успішної зміни пароля
    path('profile/change-password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    #admin profile
    path('admin-my-data.html', views.admin_my_data, name='admin_my_data'),
    path('admin-guests.html', views.admin_guests, name='admin_guests'),
    path('admin-rooms.html', views.admin_rooms, name='admin_rooms'),
    path('admin-hotel-status.html', views.admin_hotel_status, name='admin_hotel_status'),
    path('admin-reservations.html', views.admin_reservations, name='admin_reservations'),
    path('admin-workers.html', views.admin_workers, name='admin_workers'),
    path('admin-create-employee.html', views.admin_create_employee, name='admin_create_employee'),
    path('admin-create-room.html', views.admin_create_room, name='admin_create_room'),
    
    #user profile
    path('user-my-data.html', views.user_my_data, name='user_my_data'),
    path('user-reservations.html', views.user_reservations, name='user_reservations'),
    path('user-book-room.html', views.user_book_room, name='user_book_room'),
    path('user-reservation-form.html', views.user_reservation_form, name='user_reservation_form'),
    path('user-reservation-form-check.html', views.user_reservation_form_check, name='user_reservation_form_check'),
    
    path('rooms.html', views.rooms, name='rooms'),
]
