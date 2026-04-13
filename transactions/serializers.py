from rest_framework import serializers
from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'color']
        read_only_fields = ['id']

    def validate_color(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError("Color must be a valid hex code e.g. #FF5733")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'category', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_category(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("Category does not belong to the authenticated user.")
        return value

    def validate(self, data):
        category = data.get('category')
        if category and data.get('type') != category.type:
            raise serializers.ValidationError(
                "Transaction type must match the category type."
            )
        return data