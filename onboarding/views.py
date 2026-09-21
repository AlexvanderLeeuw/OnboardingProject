from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from onboarding.models import Category, Expense, Income
from onboarding.serializers import CategorySerializer, ExpenseSerializer, IncomeSerializer
from onboarding.choice_lists import CURRENCY_CHOICES
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
import re

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

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

class GetAuthToken(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = Token.objects.get(user=request.user)
            return Response({'token': token.key})
        except Token.DoesNotExist:
            return Response({'token': None}, status=400)

def protected_page(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login-page')
        return view_func(request, *args, **kwargs)
    return wrapper

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one capital letter')
    if not re.search(r'[0-9]', password):
        errors.append('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        errors.append('Password must contain at least one special character')
    return errors

#Template views start here
@protected_page
def categories_page(request):
    return render(request, "onboarding/categories.html")

@protected_page
def expenses_page(request):
    return render(request, "onboarding/expenses.html", {"currency_choices": CURRENCY_CHOICES})

@protected_page
def expense_details_page(request, pk):
    return render(request, "onboarding/expensedetails.html", {"currency_choices": CURRENCY_CHOICES, "expense_id": pk})

@protected_page
def incomes_page(request):
    return render(request, "onboarding/incomes.html", {"currency_choices": CURRENCY_CHOICES})

@protected_page
def income_details_page(request, pk):
    return render(request, "onboarding/incomedetails.html", {"currency_choices": CURRENCY_CHOICES, "income_id": pk})

@protected_page
def monthly_expenses_page(request):
    return render(request, "onboarding/monthlyexpenses.html", {"currency_choices": CURRENCY_CHOICES})

@protected_page
def monthly_incomes_page(request):
    return render(request, "onboarding/monthlyincomes.html", {"currency_choices": CURRENCY_CHOICES})

@protected_page
def expense_income_comparison_page(request):
    return render(request, "onboarding/expenseincomecomparison.html", {"currency_choices": CURRENCY_CHOICES})

@require_http_methods(["GET", "POST"])
def login_page(request):
    if request.user.is_authenticated:
        return redirect('categories-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('categories-page')
        else:
            return render(request, 'onboarding/login.html', {'error': 'Invalid username or password'})

    return render(request, 'onboarding/login.html')

@require_http_methods(["GET", "POST"])
def register_page(request):
    if request.user.is_authenticated:
        return redirect('categories-page')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        password_errors = validate_password(password)
        if password_errors:
            return render(request, 'onboarding/register.html', {'error': password_errors[0]})

        if password != password_confirm:
            return render(request, 'onboarding/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'onboarding/register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'onboarding/register.html', {'error': 'Email already exists'})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('categories-page')
        except IntegrityError:
            return render(request, 'onboarding/register.html', {'error': 'Error creating account'})

    return render(request, 'onboarding/register.html')

def logout_page(request):
    logout(request)
    return redirect('login-page')

def token_error_page(request):
    return render(request, 'onboarding/token_error.html')

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_405(request, exception):
    return render(request, 'errors/405.html', status=405)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
