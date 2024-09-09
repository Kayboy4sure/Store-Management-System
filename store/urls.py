from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<int:pk>/', views.update_items, name='update_items'),
    path('delete_items/<int:pk>/', views.delete_items, name='delete_items'),
    path('store_items/<int:pk>/', views.store_items, name='store_items'),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('history/', views.history, name="history"),
]