from rest_framework import serializers
from onboarding.models import Category, Income, Expense

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "owner", "name"]
        read_only_fields = ["id", "owner"]

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]
    def validate_category(self, category):
        if category.owner != self.context["request"].user:
            raise serializers.ValidationError(
                "Category belongs to other user."
            )
        return category

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]
    def validate_category(self, category):
            if category.owner != self.context["request"].user:
                raise serializers.ValidationError(
                    "Category belongs to other user."
                )
            return category
