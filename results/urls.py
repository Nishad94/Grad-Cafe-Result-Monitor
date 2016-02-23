from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/',views.logoutUser, name='logout'),
    url(r'^updateDB/', views.updateDB, name='updateDB'),
    url(r'^register/', views.register, name='register'),
    #url(r'^register_new/', views.register_new, name='register_new'),
    url(r'^welcome/', views.welcomeUser, name='welcome'),
    url(r'^save_college/', views.save_college, name='save_college'),
    url(r'^listOfColleges/', views.listOfColleges, name='listOfColleges'),
    url(r'^swapSubscription/', views.swapSubscription, name='swapSubscription'),
    url(r'^deleteColleges/', views.deleteColleges, name='deleteColleges')
]