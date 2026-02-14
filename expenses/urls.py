from django.urls import path
from .views import AddExpenseView,ListExpensesView, UpdateExpenseView,DeleteExpenseView

urlpatterns = [
    path('add/', AddExpenseView.as_view()),
    path('list/', ListExpensesView.as_view()),
    path('update/<int:pk>/', UpdateExpenseView.as_view()),
    path('delete/<int:pk>/', DeleteExpenseView.as_view()),
]