from django.urls import path
from .import views

app_name='cbt'

urlpatterns=[
    path('',views.HomeView.as_view(),name='home'),
    path('question/<int:pk>',views.QuestionView.as_view(),name="question"),
    path('updatelist/',views.UpdateList.as_view(),name="updatelist"),
    path('update/<int:pk>',views.QuestionUpdate.as_view(),name="update")
    ]