from rest_framework import serializers
from .models import Message


class ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('read',)
        read_only_fields = ('receiver','subject', 'message')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'url', 'sender', 'receiver', 'subject', 'message', 'created_at', 'read')
        read_only_fields = ('sender','read')

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
    