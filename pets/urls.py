from django.urls import path
from pets.views import PetView, PetViewUnique


urlpatterns = [
    path('pets/', PetView.as_view()),
    path('pets/<int:pet_id>/', PetViewUnique.as_view())
]
