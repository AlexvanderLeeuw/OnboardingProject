from django.urls import path
from onboarding import views

urlpatterns = [
    #API
    path('api/categories/', views.CategoryList.as_view(), name='category-list'),
    path('api/categories/<int:pk>', views.CategoryDetails.as_view(), name='category-detail'),
    path('api/expenses/', views.ExpenseList.as_view(), name='expense-list'),
    path('api/expenses/<int:pk>', views.ExpenseDetails.as_view(), name='expense-detail'),
    path('api/incomes/', views.IncomeList.as_view(), name='income-list'),
    path('api/incomes/<int:pk>', views.IncomeDetails.as_view(), name='income-detail'),

    #Templates
    path('categories/', views.categories_page, name='categories-page'),
]
