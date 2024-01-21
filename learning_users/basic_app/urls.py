from django.urls import path,include
from basic_app import views

# Template URLS 
app_name = 'basic_app'

urlpatterns = [
   path('register/',views.register ,name='register'),
   path('log_in',views.log_in,name='log_in'),

]
