from django.urls import path
from . import views

urlpatterns = [
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcements/<int:announcement_pk>/responses/<int:response_pk>/accept/',
         views.accept_response, name='accept_response'),
    path('responses/', views.user_responses, name='user_responses'),
    path('responses/<int:response_id>/delete/', views.delete_response, name='delete_response'),
    path('categories/<int:category_id>/', views.category_announcements, name='category_announcements'),
]
