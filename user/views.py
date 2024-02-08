from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer, UserManageSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for managing user profile information.

    Allows authenticated users to retrieve and update their own user profile information.
    """

    serializer_class = UserManageSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    """
    API endpoint for creating new users.

    Allows unauthenticated users to create a new user account.
    """

    serializer_class = UserSerializer
