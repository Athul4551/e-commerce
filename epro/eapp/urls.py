from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
  path('',views.firstpage,name="firstpage"),
  path('seller',views.sellerlogin,name='sellerlogin'),
  path('signup',views.sellersignup,name='sellersignup'),
  path('forgotpassword',views.getusername,name='forgotpassword'),
  path('verifyotp',views.verifyotp,name='verifyotp'),
  path('passwordreset',views.passwordreset,name='passwordreset'),
  path('index',views.index,name='index'),
  path('logout',views.logoutuser,name="logout"),
  path('firstpage',views.firstpage,name="firstpage"),
  path('userlogin',views.userlogin,name="userlogin"),
  path('usersignup',views.usersignup,name="usersignup"),
  path('deletion/<int:id>',views.delete_g,name='deletion'),
  path('add',views.add,name='add'),
  path('sellerfirstpage',views.sellerfirstpage,name='sellerfirstpage'),
  path('edit_g/<int:id>',views.edit_g,name='edit_g'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)