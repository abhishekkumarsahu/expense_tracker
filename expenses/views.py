from django.shortcuts import render
from datetime import date,timedelta

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer
from .models import Expense

class AddExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        filter_type = Expense.query_paras.get('filter')
        start_date = Expense.query_paras.get('start')
        end_date = Expense.query_paras.get('end')

        expenses = Expense.objects.filter(user=request.user)
        # serializer = ExpenseSerializer(expenses, many=True)
        # return Response(serializer.data)
    
        today = date.today()

        if filter_type == "past_week":
            expenses = Expense.filter(date_gte=today - timedelta(days=7))
        
        elif filter_type == "past_month":
            expenses =  Expense.filter(date__gte=today - timedelta(days=30))

        elif filter_type == "past_3_months":
            expenses = Expense.filter(date__range=[start_date, end_date])

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
        
from django.shortcuts import get_object_or_404

class UpdateExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, user=request.user)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, user=request.user)
        expense.delete()
        return Response({"message": "Deleted successfully"}, status=204)
    
# def validate_amount(self, value):
#     if value <= 0:
#         raise serializers.ValidationError("Amount must be greater than zero.")
#     return value