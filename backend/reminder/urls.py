from django.urls import path
from .views import AiAssistantApiView
urlpatterns = [
    path('assignment-reminder/',AiAssistantApiView.as_view(),name="assignment-reminder")
    
]