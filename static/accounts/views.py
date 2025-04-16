from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .choices import UserTypeChoices
from .models import CustomUser
from .serializers import UserSerializer

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

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserTypeChoices.ADMIN:
            return CustomUser.objects.all()
        elif user.user_type == UserTypeChoices.STUDENT:
            return CustomUser.objects.filter(id=user.id)
        return CustomUser.objects.none()