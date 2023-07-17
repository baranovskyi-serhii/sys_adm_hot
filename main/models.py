from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import datetime

"""@receiver(post_migrate)
def create_default_user_type(sender, **kwargs):
    if sender.name == 'main':
        user_type_name = 'user'
        user_type, created = UserType.objects.get_or_create(user_type_name=user_type_name)
        if created:
            print(f"Created user type: {user_type_name}")
        else:
            print(f"User type already exists: {user_type_name}")

        Customer.objects.filter(user_type=None).update(user_type=user_type)"""

class Customer(AbstractUser):
    customer_id = models.AutoField(primary_key=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.ForeignKey('UserType', null=True, blank=True, on_delete=models.PROTECT, default=None)

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.customer_id)])

    def __str__(self):
        return '({0}) {1} {2}'.format(self.customer_id, self.first_name, self.last_name)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customer_set',  # змінений related_name
        related_query_name='Customer'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customer_set',  # змінений related_name
        related_query_name='Customer'
    )


class UserType(models.Model):
    user_type_id = models.AutoField(primary_key=True)
    user_type_name = models.CharField(max_length=50)
    lock_type = models.BooleanField(blank=True, null=True, default=False)
    
    def __str__(self):
        return self.user_type_name


class Reservation(models.Model):
    """Моделі для бронювання"""
    reservation_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,  related_name='reservations_as_customer' )
    no_of_children = models.PositiveSmallIntegerField(default=0)
    no_of_adults = models.PositiveSmallIntegerField(default=1)
    reservation_date_time = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(default=timezone.now)
    cancel = models.BooleanField(default=0)
    
    class Meta:
        permissions = ( 
                        ('can_view_reservation', 'Можна переглянути бронювання'),
                        ('can_view_reservation_detail', 'Можна переглянути деталі бронювання'),
                    )

    def get_absolute_url(self):
        return reverse('reservation-detail', args=str([self.reservation_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.reservation_id, self.customer.first_name, self.customer.last_name)


class Faciliti(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()
    
    class Meta:
        verbose_name_plural = 'Зручності'  # В іншому випадку на панелі адміністратора буде показано Facilities

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='room_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.image.url}"


class Room(models.Model):
    room_no = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    room_type = models.ForeignKey('RoomType', null=False, blank=True, on_delete=models.CASCADE)
    availability = models.BooleanField(default=0)
    booked = models.BooleanField(default=0)
    conveniences = models.ManyToManyField('Faciliti', related_name='conveniences')
    staff = models.ForeignKey('Customer', on_delete=models.CASCADE, editable=True, related_name='rooms_as_staff')
    adult_count = models.IntegerField(default=0)
    child_count = models.IntegerField(default=0)
    images = models.ManyToManyField('Image', related_name='images')
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['room_no', ]
        permissions = (('can_view_room', 'Можна переглянути кімнату'),)

    def __str__(self):
        return "%s - %s - Rs. %i" % (self.room_no, self.room_type.name, self.room_type.price)

    def display_facility(self):
        return ', '.join([faciliti.name for faciliti in self.conveniences.all()])

    display_facility.short_description = 'Зручності'
    
    def display_images(self):
        return ', '.join([image.__str__() for image in self.images.all()])

    display_images.short_description = 'Зображення'

    def get_absolute_url(self):
        return reverse('room-detail', args=[self.room_no])

    def save(self, *args, **kwargs):  # Перевизначення типової поведінки збереження

        super().save(*args, **kwargs)


class RoomType(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name