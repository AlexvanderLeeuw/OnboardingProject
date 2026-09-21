from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from onboarding.models import Category, Expense, Income
from onboarding.serializers import CategorySerializer, ExpenseSerializer, IncomeSerializer
from django.shortcuts import render

class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user).order_by("name")
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

class ExpenseList(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExpenseDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)

class IncomeList(ListCreateAPIView):
    serializer_class = IncomeSerializer
    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class IncomeDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user)

#Template views start here
def categories_page(request):
    return render(request, "onboarding/categories.html")
