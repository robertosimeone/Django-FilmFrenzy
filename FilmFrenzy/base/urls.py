from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/',views.logout_user,name ='logout'),
    path('',views.home,name='homepage'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('movie_list/',views.movie_list,name = 'movie_list'),
    path('movie_list/<int:pk>',views.movie,name='movie'),
    path('register/',views.register_user,name='register'),
    path('update_profile/<int:pk>',views.update_profile,name = 'update_profile'),
    path('add_funds/',views.add_funds,name="add_funds"),
    path('add_funds_manually/',views.add_funds_manually,name="add_funds_manually"),
    path('checkout/<int:pk>',views.checkout,name='checkout'),
    path('complete/',views.paymentComplete,name='complete'),
    # path('todo/<int:pk>',views.todo,name='todo'),
    

    #path('profile/',)

]
