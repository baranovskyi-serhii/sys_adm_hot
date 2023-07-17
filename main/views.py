from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, UserType, Faciliti, RoomType, Room, Reservation
from django.contrib import messages
from django.db.models import Q
from .forms import LoginForm
from .forms import RegistrationForm, CreateEmployeeForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.paginator import Paginator

from .forms import ForgotPasswordForm

from django.urls import reverse

import os
from django.http import Http404, HttpResponseRedirect

from datetime import datetime

from django.http import JsonResponse

import json

def index(request):
    return render(request, 'index.html', {})

@login_required
def view_profile(request):
    context = {}
    #return render(request, 'profile.html', context)
    if request.user.is_superuser:
        return redirect('admin_my_data')
    else:
        return redirect('user_my_data')

#!ADMIN

@login_required
def admin_my_data(request):
    context = {}
    return render(request, 'profile_admin_pages/my-data.html', context)

@login_required
def admin_guests(request):
    context = {}
    if 'page' in request.GET:
        current_page = int(request.GET['page'])
    else:
        current_page = 1

    if 'step' in request.GET:
        step = int(request.GET['step'])
    else:
        step = 10
    if step > 1000:
        step = 1000
        
    if 'user_id' in request.GET:
        user_id = int(request.GET['user_id'])
    else:
        user_id = -1
    
    if user_id != -1:
        users = Customer.objects.filter(customer_id=user_id) 
    else:
        users = Customer.objects.filter(user_type__user_type_name='user')
    
    paginator = Paginator(users, step)
    users_page = paginator.get_page(current_page)

    previous_page = users_page.previous_page_number() if users_page.has_previous() else None
    next_page = users_page.next_page_number() if users_page.has_next() else None

    all_count_page = paginator.count
    
    context['users'] = users_page
    context['current_page'] = current_page
    context['previous_page'] = previous_page
    context['next_page'] = next_page
    context['step'] = step
    context['all_count_page'] = all_count_page
    showing_pages = ""
    if current_page + step <= all_count_page:
        showing_pages = '-'.join([str(current_page), str(current_page + step)])
    else:
        showing_pages = '-'.join([str(current_page), str(all_count_page)])
    
    context['showing_pages'] = showing_pages
    
    return render(request, 'profile_admin_pages/guests.html', context)

@login_required
def admin_rooms(request):
    context = {}
    if 'page' in request.GET:
        current_page = int(request.GET['page'])
    else:
        current_page = 1

    if 'step' in request.GET:
        step = int(request.GET['step'])
    else:
        step = 10
    if step > 1000:
        step = 1000
    
    if 'room_no' in request.GET:
        room_no = int(request.GET['room_no'])
        rooms = Room.objects.filter(room_no=room_no)
    else:
        rooms = Room.objects.all()
    
    paginator = Paginator(rooms, step)
    rooms_page = paginator.get_page(current_page)

    previous_page = rooms_page.previous_page_number() if rooms_page.has_previous() else None
    next_page = rooms_page.next_page_number() if rooms_page.has_next() else None

    all_count_page = paginator.count
    
    context['rooms'] = rooms_page
    context['current_page'] = current_page
    context['previous_page'] = previous_page
    context['next_page'] = next_page
    context['step'] = step
    context['all_count_page'] = all_count_page
    showing_pages = ""
    if current_page + step <= all_count_page:
        showing_pages = '-'.join([str(current_page), str(current_page + step)])
    else:
        showing_pages = '-'.join([str(current_page), str(all_count_page)])
    
    context['showing_pages'] = showing_pages
    
    return render(request, 'profile_admin_pages/rooms.html', context)


@login_required
def admin_hotel_status(request):
    context = {
        'facility_count': Faciliti.objects.count(),
        'roomtype_count': RoomType.objects.count(),
        'room_count': Room.objects.count(),
        'reservation_count': Reservation.objects.exclude(cancel=1).count(),
        'customer_count': Customer.objects.filter(user_type__user_type_name = 'user').count(),
    }
    return render(request, 'profile_admin_pages/hotel-status.html', context)

@login_required
def admin_reservations(request):
    context = {}
    
    if request.method == "POST":
        if 'tupe_req' in request.POST:
            if request.POST['tupe_req'] == 'cancel':
                if 'reservation_id' in request.POST:
                    reservation_id = request.POST['reservation_id']
                    try:
                        reservation = Reservation.objects.get(reservation_id=reservation_id)
                        reservation.delete()
                        # Додайте код для повернення відповідного відгуку або перенаправлення на іншу сторінку
                    except Reservation.DoesNotExist:
                        # Додайте код для обробки випадку, коли запис з таким reservation_id не існує
                        pass
                    
    if 'customer_id' in request.GET:
        customer_id = int(request.GET['customer_id'])
    else:
        customer_id = -1
    if customer_id != -1:
        reservations = Reservation.objects.filter(customer__customer_id=customer_id)
    else:
        reservations = Reservation.objects.all()
    context['reservations'] = reservations
    
    return render(request, 'profile_admin_pages/reservations.html', context)

@login_required
def admin_workers(request):
    context = {}
    if 'page' in request.GET:
        current_page = int(request.GET['page'])
    else:
        current_page = 1

    if 'step' in request.GET:
        step = int(request.GET['step'])
    else:
        step = 10
    if step > 1000:
        step = 1000
    
    
    users = Customer.objects.filter(user_type__user_type_name='staff')
    
    paginator = Paginator(users, step)
    users_page = paginator.get_page(current_page)

    previous_page = users_page.previous_page_number() if users_page.has_previous() else None
    next_page = users_page.next_page_number() if users_page.has_next() else None

    all_count_page = paginator.count
    
    context['users'] = users_page
    context['current_page'] = current_page
    context['previous_page'] = previous_page
    context['next_page'] = next_page
    context['step'] = step
    context['all_count_page'] = all_count_page
    showing_pages = ""
    if current_page + step <= all_count_page:
        showing_pages = '-'.join([str(current_page), str(current_page + step)])
    else:
        showing_pages = '-'.join([str(current_page), str(all_count_page)])
    
    context['showing_pages'] = showing_pages
    
    return render(request, 'profile_admin_pages/workers.html', context)

@login_required
def admin_create_employee(request):
    context = {}
    context['back_img_normal'] = "/images/create-account-office.jpeg"
    context['back_img_dark'] = "/images/create-account-office-dark.jpeg"
    context['user_types'] = UserType.objects.all()
    if request.method == 'POST':
        print(request.POST)
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = CreateEmployeeForm()
    context['form'] = form
        
    return render(request, 'profile_admin_pages/create-employee.html', context)

@login_required
def admin_create_room(request):
    context = {}
    context['back_img_normal'] = "/images/create-account-office.jpeg"
    context['back_img_dark'] = "/images/create-account-office-dark.jpeg"
    context['user_types'] = UserType.objects.all()
    return render(request, 'profile_admin_pages/create-room.html', context)
    

#!USER

@login_required
def user_my_data(request):
    context = {}
    return render(request, 'profile_user_pages/my-data.html', context)

@login_required
def user_reservations(request):
    context = {}
    
    if request.method == "POST":
        print(request.POST)
        if 'tupe_req' in request.POST:
            if request.POST['tupe_req'] == 'cancel':
                if 'reservation_id' in request.POST:
                    reservation_id = request.POST['reservation_id']
                    try:
                        reservation = Reservation.objects.get(reservation_id=reservation_id)
                        reservation.delete()
                        # Додайте код для повернення відповідного відгуку або перенаправлення на іншу сторінку
                    except Reservation.DoesNotExist:
                        # Додайте код для обробки випадку, коли запис з таким reservation_id не існує
                        pass
    
    customer_id = request.user.customer_id
    reservations = Reservation.objects.filter(customer__customer_id=customer_id, cancel=False)

    context['reservations'] = reservations
    return render(request, 'profile_user_pages/reservations.html', context)

@login_required
def user_book_room(request):
    context = {}
    return render(request, 'profile_user_pages/book-room.html', context)

@login_required
def user_reservation_form(request):
    context = {}
    
    if request.method == 'GET':
        if not 'room_no' in request.GET:
            return redirect('user_my_data')

        if 'room_no' in request.GET:
            room_no = request.GET['room_no']
        context['room_no'] = room_no 
        try:
            room = Room.objects.get(room_no=room_no)
            # Ваш код з обробкою знайденого об'єкта room
        except Room.DoesNotExist:
            room = None
        except Room.MultipleObjectsReturned:
            room = None
            
        reservations = Reservation.objects.filter(room__room_no=room_no)
        context["reservations"] = reservations
        #print(room)
        context['room'] = room
    
    if request.method == 'POST':
        print(request.POST)
        query_dict = dict(request.POST)
        start_date_str = query_dict.get('start')[0]
        end_date_str = query_dict.get('end')[0]
        room_no = query_dict.get('room_no')[0]
        no_of_children = int(query_dict.get('no_of_children')[0])
        no_of_adults = int(query_dict.get('no_of_adults')[0])
        room = Room.objects.get(room_no=room_no)
        room.booked = 0

        # Використання поточної дати, якщо вхідні дати порожні
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date() if start_date_str else datetime.now()
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date() if end_date_str else datetime.now()
        
        reservation = Reservation(customer=request.user, no_of_children=no_of_children, no_of_adults=no_of_adults, room=room, check_in_time=start_date, check_out_time=end_date)
        reservation.save()
        return redirect('user_reservations')
    else:
        return render(request, 'profile_user_pages/reservation-form.html', context)








def view_create_account(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                # Реєстрація успішна, перенаправлення на головну сторінку
                return redirect('index')
        else:
            form = RegistrationForm()
        context = {
            'form': form
        }
        context['back_img_normal'] = "/images/create-account-office.jpeg"
        context['back_img_dark'] = "/images/create-account-office-dark.jpeg"
        context['user_types'] = UserType.objects.all()
        
        return render(request, 'create-account.html', context)



def view_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        context = {}
        context['back_img_normal'] = "/images/login-office.jpeg"
        context['back_img_dark'] = "/images/login-office-dark.jpeg"
        
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email_or_username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                customers = Customer.objects.filter(email=email_or_username) | Customer.objects.filter(username=email_or_username)

                if customers.exists():
                    customer = customers.first()
                    if customer.check_password(password):
                        customer.backend = 'main.backends.CustomUserBackend'
                        login(request, customer)
                        return redirect('index')
                    else:
                        messages.error(request, 'Невірний логін або пароль')
                else:
                    messages.error(request, 'Такого користувача не існує')
                    
                context['form'] = form
                return render(request, 'login.html', context)
        else:
            form = LoginForm()

        context['form'] = form
        return render(request, 'login.html', context)

def view_logout(request):
    logout(request)
    return redirect('index')




class ForgotPasswordView(PasswordResetView):
    template_name = 'forgot-password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_img_normal'] = "/images/forgot-password-office.jpeg"
        context['back_img_dark'] = "/images/forgot-password-office-dark.jpeg"
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        customers = Customer.objects.filter(email=email)

        if customers.exists():
            customer = customers.first()
            customer_id = customer.customer_id
        
            # Перевірка, чи існує користувач з введеним email
            # Якщо так, відправте лист з інструкціями щодо скидання пароля
            # Якщо немає, відображайте повідомлення про помилку
            # Використовуйте функцію render_to_string для збірки шаблону електронного листа
            # Ви можете використовувати urlsafe_base64_encode та force_bytes для генерації посилання скидання пароля
            # Використовуйте функцію send_mail для надсилання електронного листа
            # Приклад:
            
            token = urlsafe_base64_encode(force_bytes(customer_id))
            reset_link = self.request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': token, 'token': token}))
            email_subject = 'Скидання пароля'
            styles = ""
            try:
                # Отримання абсолютного шляху до поточного файла views.py
                current_file_path = os.path.abspath(__file__)

                # Отримання шляху до директорії, в якій знаходиться поточний файл
                current_directory = os.path.dirname(current_file_path)

                # Формування шляху до файлу стилів відносно поточної директорії
                styles_file_path = os.path.join(current_directory, 'static/css/tailwind.css')
                
                with open(styles_file_path, 'r') as file:
                    styles = file.read()
            except Exception as ex:
                styles = ""

            
            email_message = render_to_string('password_reset_email.html', {'reset_link': reset_link, 'styles': styles})
            """send_mail(
                email_subject,
                email_message,
                'ggcombaall@gmail.com',
                [email],
                fail_silently=False,
            )"""

            messages.success(self.request, 'Лист для скидання пароля був надісланий на вашу електронну адресу.')
        else:
            messages.error(self.request, 'Користувача не знайдено.')
        return super().form_valid(form)
        #return HttpResponseRedirect(self.get_success_url())
            

def view_forgot_password(request):
    return ForgotPasswordView.as_view()(request)



def rooms(request):
    context = {}
    try:
        if 'page' in request.GET:
            current_page = int(request.GET['page'])
        else:
            current_page = 1
    except:
        current_page = 1
    try:
        if 'step' in request.GET:
            step = int(request.GET['step'])
        else:
            step = 6
    except:
        step = 6
    if step > 1000:
        step = 1000
    
    if request.method == 'POST':
        #print(request.POST)
        query_dict = dict(request.POST)
        # print(query_dict)
        start_date_str = query_dict.get('start', [''])[0]
        end_date_str = query_dict.get('end', [''])[0]

        try:
            no_of_children = int(query_dict.get('child', [-1])[0])
        except ValueError:
            no_of_children = -1
        try:
            no_of_adults = int(query_dict.get('adult', [-1])[0])
        except ValueError:
            no_of_adults = -1

        print(f"{start_date_str} {end_date_str} {no_of_adults} {no_of_children}")
        
        if start_date_str != '' and end_date_str != '':
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
        else:
            start_date = None
            end_date = None

        reservations = None

        if start_date is not None and end_date is not None:
            reservations = Reservation.objects.filter(
                check_in_time__date__gt=start_date,
                check_out_time__date__lt=end_date
            )
        if reservations is not None:
            rooms_in_reservations = reservations.values_list('room', flat=True)
            rooms = Room.objects.exclude(room_no__in=rooms_in_reservations)
        else:
            rooms = Room.objects.all()
        
        if no_of_children != -1:
            rooms = rooms.filter(child_count=no_of_children)

        if no_of_adults != -1:
            rooms = rooms.filter(adult_count=no_of_adults)

    else:               
        rooms = Room.objects.all()
    
    paginator = Paginator(rooms, step)
    rooms_page = paginator.get_page(current_page)

    previous_page = rooms_page.previous_page_number() if rooms_page.has_previous() else None
    next_page = rooms_page.next_page_number() if rooms_page.has_next() else None

    all_count_page = paginator.count
    
    context['rooms'] = rooms_page 
    context['current_page'] = current_page
    context['previous_page'] = previous_page
    context['next_page'] = next_page
    context['step'] = step
    context['all_count_page'] = all_count_page
    showing_pages = ""
    if current_page + step <= all_count_page:
        showing_pages = '-'.join([str(current_page), str(current_page + step)])
    else:
        showing_pages = '-'.join([str(current_page), str(all_count_page)])
    
    context['showing_pages'] = showing_pages
    
    return render(request, 'rooms.html', context)

@login_required
def user_reservation_form_check(request):
    if request.method == 'POST':
        status = False
        json_data = json.loads(request.body)
        start = json_data.get('start')
        end = json_data.get('end')
        room_no = json_data.get('room_no')
        try:
            no_of_children = int(json_data.get('no_of_children'))
        except:
            no_of_children = -1
            
        try:  
            no_of_adults = json_data.get('no_of_adults')
        except:
            no_of_adults = -1
        
        if start == '' or end == '' or room_no == '':
            status = False
            print(f"EMPTY {json_data}")
        else:
            start_date_str = start
            end_date_str = end
            room_no = int(room_no)
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date() if start_date_str else datetime.now()
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date() if end_date_str else datetime.now()
            if no_of_children != -1 and no_of_adults != -1:
                reservations = Reservation.objects.filter(
                    Q(check_in_time__date__gte=start_date), 
                    Q(check_out_time__date__lte=end_date), 
                    room__room_no=room_no,
                    no_of_children =no_of_children,
                    no_of_adults=no_of_adults
                )
            elif no_of_children != -1 and no_of_adults == -1:
                reservations = Reservation.objects.filter(
                    Q(check_in_time__date__gte=start_date), 
                    Q(check_out_time__date__lte=end_date), 
                    room__room_no=room_no,
                    no_of_children =no_of_children
                )
            elif no_of_children == -1 and no_of_adults != -1:  
                reservations = Reservation.objects.filter(
                    Q(check_in_time__date__gte=start_date), 
                    Q(check_out_time__date__lte=end_date), 
                    room__room_no=room_no,
                    no_of_adults=no_of_adults
                )
            else:
                reservations = Reservation.objects.filter(
                    Q(check_in_time__date__gte=start_date), 
                    Q(check_out_time__date__lte=end_date), 
                    room__room_no=room_no
                )
                
            rooms = reservations.values_list('room', flat=True)
            print(rooms)
            status = False
            try:
                if len(rooms) > 0:
                    for single_room in rooms:
                        if int(single_room.room_no) == int(room_no):
                            status = True
                        else:
                            status = False
                else:
                    status = True
            except Exception as ex:
                print(ex)
            print(json_data)

        response_data = {
            'status': status,
        }
        return JsonResponse(response_data)