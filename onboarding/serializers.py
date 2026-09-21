from rest_framework import serializers
from onboarding.models import Category, Income, Expense

class CategorySerializer(serializers.ModelSerializer):
    #Check if the user doesn't already have a category with the same name
    def validate_name(self, name):
        user = self.context["request"].user

        if Category.objects.filter(owner=user, name=name).exists():
            raise serializers.ValidationError("You already have a category with this name.")
        return name

    class Meta:
        model = Category
        fields = ["id", "owner", "name"]
        read_only_fields = ["id", "owner"]

class IncomeSerializer(serializers.HyperlinkedModelSerializer):
    #Make sure that the category and owner fields show up as names, not IDs
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    #In init, give the category a queryset that filters to the user
    #Cant be done in the initial SlugRelatedField because self doesn't exist yet by then
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)
    #Make sure that a user can't add an income of 0 or less.
    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Income must have earn than 0.")
        return amount
    #Return an error if the user attempts to add an income with the same source, amount and date for duplicate protection, asking to number the source if it was intentional
    def validate(self, attrs):
        user = self.context["request"].user    
        duplicate = Income.objects.filter(
            owner=user, 
            source=attrs.get("source"), 
            amount=attrs.get("amount"), 
            date=attrs.get("date"),
        )
        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise serializers.ValidationError("Identical income already exists. To protect against accidental duplicate entries, please add numbering at end of source if this was intentional")
        return attrs

    class Meta:
        model = Income
        fields = ["id", "url", "source", "category", "currency", "amount", "date", "owner"]
        read_only_fields = ["id", "owner"]

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    #Make sure that the category and owner fields show up as names, not IDs
    category = serializers.SlugRelatedField(read_only=False, slug_field="name", queryset=Category.objects.all())
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    #In init, give the category a queryset that filters to the user
    #Cant be done in the initial SlugRelatedField because self doesn't exist yet by then
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = Category.objects.filter(owner=user)
    #Make sure that a user can't add an expense of 0 or less.
    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Expense must have a cost greater than 0.")
        return amount
    #Return an error if the user attempts to add an expense with the same source, amount and date for duplicate protection, asking to number the source if it was intentional
    def validate(self, attrs):
        user = self.context["request"].user    
        duplicate = Expense.objects.filter(
            owner=user, 
            source=attrs.get("source"), 
            amount=attrs.get("amount"), 
            date=attrs.get("date"),
        )
        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise serializers.ValidationError("Identical expense already exists. To protect against accidental duplicate entries, please add numbering at end of source if this was intentional")
        return attrs

    class Meta:
        model = Expense
        fields = ["id", "url", "source", "category", "currency", "amount", "date", "repeats", "owner"]
        read_only_fields = ["id", "owner"]
