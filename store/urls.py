from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
     path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
  #  path('update/',views.update_user,name='update_user'),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>',views.category,name='category'),
    
]
