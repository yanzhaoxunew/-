from .views import *
from django.urls import path

urlpatterns = [
    path('book/', CreateBookingView.as_view(), name='create-booking'),
    path('daily-report/', DailyReportView.as_view(), name='daily-report'),
    path('personal-booking/', PersonalBookingView.as_view(), name='personal-booking'),
    path('cancel-booking/', CancelBookingView.as_view(),{'method':'POST'}, name='cancel-booking'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('user-list/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]