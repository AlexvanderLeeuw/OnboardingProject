from django.urls import path
from onboarding import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>', views.CategoryDetails.as_view(), name='category-details'),
    path('expenses/', views.ExpenseList.as_view(), name='expense-list'),
    path('expenses/<int:pk>', views.ExpenseDetails.as_view(), name='expense-details'),
    path('incomes/', views.IncomeList.as_view(), name='income-list'),
    path('incomes/<int:pk>', views.IncomeDetails.as_view(), name='income-details'),
]
