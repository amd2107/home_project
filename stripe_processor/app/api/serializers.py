from rest_framework import serializers

class ProcessCardSerializer(serializers.Serializer):
    card = serializers.CharField(min_length=15, max_length=16)
    cvv = serializers.CharField(min_length=3, max_length=4)
    date = serializers.CharField(min_length=4, max_length=4)
    transaction_id = serializers.CharField(min_length=1, max_length=15)
