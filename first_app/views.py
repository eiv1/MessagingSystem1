# Messaging system- Python, Django
# Aviya yahav

from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer, ReadSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class UnReadMessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(receiver=user) & Q(read=False))

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.sender or request.user == instance.receiver:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.receiver:
            serializer = ReadSerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(sender=user) | Q(receiver=user))