from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
