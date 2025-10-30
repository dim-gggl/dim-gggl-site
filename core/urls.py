from django.urls import path
from .views import HomeView, AboutView, ContactView, CompetencesView


app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('skills/', CompetencesView.as_view(), name='skills'),
    path('contact/', ContactView.as_view(), name='contact'),
]
    

