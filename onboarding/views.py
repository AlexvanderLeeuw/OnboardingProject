from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from onboarding.models import Category, Expense, Income
from onboarding.serializers import CategorySerializer, ExpenseSerializer, IncomeSerializer

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ExpenseList(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseDetals(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class IncomeList(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class IncomeDetails(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
