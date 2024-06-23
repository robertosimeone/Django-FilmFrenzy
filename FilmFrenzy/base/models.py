from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_non_negative(value):
     if value <= 0:
        raise ValidationError(
            _('%(value)s is a negative number'),
            params={'value': value},
        )
def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "default/logo_1080_1080.png"


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have a password")
        user = self.model(email=self.normalize_email(email), username=username, )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Movie(models.Model):
    name = models.CharField(verbose_name="title", max_length=90,default ='')
    duration = models.IntegerField(verbose_name="movie duration", default=0)
    description = models.TextField(verbose_name="movie description", default='')
    price = models.DecimalField(verbose_name="movie price", decimal_places=2, max_digits=5, default=0)
    image = models.ImageField(verbose_name="movie image", max_length=255, upload_to="images/", null=True, blank=True,
                              default='17-640x640.jpeg')

    def __str__(self):
        return self.name
    @property
    def my_image(self):

        if self.image :
            return self.image.url
        return '/media/images/png-transparent-clapperboard-computer-icons-film-movie-poster-angle-text-logo-thumbnail_fFfV2Vv.png'
    


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=70, unique=True)
    first_name = models.CharField(max_length = 30,default = '')
    last_name = models.CharField(max_length = 30,default = '')
    token = models.DecimalField(verbose_name="token balance", decimal_places=2, max_digits=100000, default=0)
    streak_number = models.IntegerField(verbose_name="streak number", default=0)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # get_profile_image_filepath
    # get_default_profile_image
    profile_image = models.ImageField(max_length=255, upload_to="images/", null=True, blank=True,
                                      default='17-640x640.jpeg')
    subscribed_movies = models.ManyToManyField(Movie, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# def get_profile_image_filename(self):
# return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


class Statistic(models.Model):
    movies_watched = models.IntegerField(default=0)
    movies_liked = models.IntegerField(default=0)
    comment_counter = models.IntegerField(default=0)
    likes_counter = models.IntegerField(default=0)

    user = models.ForeignKey(User, related_name="statistics", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def create_statistics(sender, instance, created, **kwargs):
    if created:
        user_statistic = Statistic(user=instance)
        user_statistic.save()


post_save.connect(create_statistics, sender=User)

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=500,blank =True)


    def __str__(self):
        return self.user.username
class Comment(models.Model):
    user = models.ForeignKey(User,related_name="commentsUser",null=True,on_delete = models.DO_NOTHING)
    movie = models.ForeignKey(Movie,related_name='commentMovie',null=True,on_delete = models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return(
            f'{self.user.username}'
            f' ({self.created_at:%Y-%m-%d %H:%M}): '
            f'{self.body}...'
        )


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(null=True,blank = True)
    description = models.TextField(null = True,blank = True)
    token_value = models.FloatField(null=True,blank=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User,related_name='order',null=True,on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    product = models.ForeignKey(Product,max_length=200,null=True,blank=True,on_delete=models.DO_NOTHING)
    def __str__(self):
        return f'{self.id} Order'

class OrderManually(models.Model):
    user = models.ForeignKey(User,related_name='ordermanually',on_delete=models.CASCADE)
    order_value = models.DecimalField(verbose_name="order_value", decimal_places=2, max_digits=1000, default=0.01,validators=[validate_non_negative])
    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return f'{id}'
class ToDOPage(models.Model):
    user = models.ForeignKey(User,related_name='todopage',on_delete = models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return user.username