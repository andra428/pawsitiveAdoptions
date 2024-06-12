"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from test_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('aboutGiving/', views.aboutGiving, name='aboutGiving'),
    path('signup/', views.singup, name='signup'),
    path('loginPagina/', views.loginPagina, name='loginPagina'),
    path('logout_view/', views.logout_view, name="logout_view"),
    path('search_pets/', views.search_pets, name='search_pets'),
    path('findPets/', views.findPets, name='findPets'),
    path('createUserAdoptator/', views.createUserAdoptator, name='createUserAdoptator'),
    path('accountView/', views.accountView, name='accountView'),
    path('showCompatibleAnimals/', views.showCompatibleAnimals, name="showCompatibleAnimals"),
    path('updateAnimalPreferencesView/', views.updateAnimalPreferencesView, name="updateAnimalPreferencesView"),
    path('updateAnimalPreferences/', views.updateAnimalPreferences, name="updateAnimalPreferences"),
    path('updatePersonalInfoView/', views.updatePersonalInfoView, name="updatePersonalInfoView"),
    path('updatePersonalInfo/', views.updatePersonalInfo, name="updatePersonalInfo"),
    path('postAnAnnouncementView/', views.postAnAnnouncementView, name="postAnAnnouncementView"),
    path('postAnAnnouncement/', views.postAnAnnouncement, name="postAnAnnouncement"),
    path('showAnimals/', views.showAnimals, name="showAnimals"),
    path('loginAdoptator/', views.loginAdoptator, name="loginAdoptator"),
    path('details/<int:idAnimal>/', views.details, name='details'),
    path('updateAnimalInfoView/<int:idAnimal>/', views.updateAnimalInfoView, name="updateAnimalInfoView"),
    path('updateAnimalInfo/<int:idAnimal>/', views.updateAnimalInfo, name='updateAnimalInfo'),
    path('considerForAdoptionView/<int:idAnimal>/',views.considerForAdoptionView, name='considerForAdoptionView'),
    path('deleteAnimal/<int:idAnimal>/', views.deleteAnimal, name="deleteAnimal"),
    path('ForwardAdopting/<int:score>/<int:idAnimal>/', views.ForwardAdopting, name="ForwardAdopting"),
    path('contactOwner/<int:idAnimal>/', views.contactOwner, name="contactOwner"),
    path('showAnimalsMessagesAdoptator/', views.showAnimalsMessagesAdoptator, name="showAnimalsMessagesAdoptator"),
    path('showAnimalsMessagesGiveToAdopt/', views.showAnimalsMessagesGiveToAdopt, name="showAnimalsMessagesGiveToAdopt"),
    path('convoAdoptator/<int:idAnimal>/', views.convoAdoptator, name="convoAdoptator"),
    path('sendMessageBack/<int:idAnimal>/', views.sendMessageBack, name="sendMessageBack"),
    path('petfinderArticlesDogs/', views.petfinderArticlesDogs, name="petfinderArticlesDogs"),
    path('petfinderArticlesCats/', views.petfinderArticlesCats, name="petfinderArticlesCats"),
    path('viewArticle/<path:link>/', views.viewArticle, name='viewArticle'),
    path('mapView',views.mapView, name="mapView")
]
