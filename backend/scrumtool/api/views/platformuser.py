from rest_framework import viewsets

from . import models
from . import serializers
from rest_framework.response import Response


class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = models.PlatformUser.objects.all()
    serializer_class = serializers.ScrumUserSerializer

    def retrieve(self, request, *args, pk=None, **kwargs):
        """retrive for full and partial retrieve
            Instead of id a username can be used
            """
        username: str = pk
        current_user: models.PlatformUser = self.request.user
        # return userinfo if user wants to access own profile
        if username is not None and username == current_user.username:
            instance = current_user
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
