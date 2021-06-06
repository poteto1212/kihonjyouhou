from django.urls import path
from .import views

app_name='cbt'

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('question/<int:pk>',views.QuestionView.as_view(),name="question")
    ]