from rest_framework import serializers
from onboarding.models import Category, Income, Expense

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "owner", "name"]
        read_only_fields = ["id", "owner"]

class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)
        
    class Meta:
        model = Income
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)

    class Meta:
        model = Expense
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]
