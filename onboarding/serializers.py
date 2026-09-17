from rest_framework import serializers
from onboarding.models import Category, Income, Expense

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "owner", "name"]
        read_only_fields = ["id", "owner"]

class IncomeSerializer(serializers.ModelSerializer):
    #Make sure that the category and owner fields show up as names, not IDs
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    #In init, give the category a queryset that filters to the user
    #Cant be done in the initial SlugRelatedField because self doesn't exist yet by then.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)
    #Make sure that a user can't add an income of 0 or less.
    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Income must have earn than 0.")
        return amount

    class Meta:
        model = Income
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]

class ExpenseSerializer(serializers.ModelSerializer):
    #Make sure that the category and owner fields show up as names, not IDs
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    #In init, give the category a queryset that filters to the user
    #Cant be done in the initial SlugRelatedField because self doesn't exist yet by then.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)
    #Make sure that a user can't add an expense of 0 or less.
    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Expense must have a cost greater than 0.")
        return amount

    class Meta:
        model = Expense
        fields = ["id", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]
