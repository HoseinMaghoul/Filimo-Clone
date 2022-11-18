import random


from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        creates and saves a user with given username, email and password
        """

        now = timezone.now()
        if not username:
            raise ValueError('you must set a username')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)


        if not extra_fields.get('no_password'):
            user.set_password(password)

            user.save(using=self._db)
            return user

    def  create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while CustomUser.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username ,phone_number, email, password, False , False, **extra_fields)


    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured user model with
    admin-compliant permissions.

    Username, password and email are required. other  fields are optional.
    """
    username = models.CharField(max_length=30, unique=True,
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$', ),
                                ],
                                error_messages={
                                    'unique': 'A user with that username already exists.'
                                })
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(unique=True, null=True, blank=True,
                                          validators=[

                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        'Enter a valid mobile number. '),

                                          ],
                                          error_messages={
                                              'unique': 'A user with this mobile number already exists. '
                                          })
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a spac in between

        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


    def get_short_name(self):
        """
        Returns the short name for the user

        """
        return self.first_name


    def email_user(self, subject, message, form_email=None, **kwargs):
        """
        Sends an email to this User

        """
        send_mail(subject, message, form_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        """
        Returns True if user actually logged in with valid credentials.

        """
        return self.phone_number is not None or self.email is not None


    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)



        



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nic_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.BooleanField(help_text=('famale is False, male is True, null is unset'), null=True)
    province = models.ForeignKey(verbose_name='province', to='province', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    @property
    def get_first_name(self):
        return self.user.first_name


    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nickname(self):
        return self.nic_name if self.nic_name else self.user.username


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(CustomUser, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(null=True)
    last_login = models.DateTimeField(null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(max_length=20, blank=True)
    device_model = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=30)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




