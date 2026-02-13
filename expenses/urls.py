from django.urls import path
from .views import AddExpenseView,ListExpensesView

urlpatterns = [
    path('add/', AddExpenseView.as_view()),
    path('list/', ListExpensesView.as_view()),
]