"""ViewSet for PlatformUser"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from . import models
from . import serializers


class PlatformUserViewSet(viewsets.ModelViewSet):
    """PlatformUser ViewSet to return data to REST api
    """
    queryset = models.PlatformUser.objects.all()

    def get_queryset(self):
        if 'task_pk' not in self.kwargs:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(
                task_cards=self.kwargs['task_pk'])
    serializer_class = serializers.PlatformUserSerializer

    def retrieve(self, request: Request, pk=None):
        """retrive for full and partial retrieve
            Instead of id a username can be used
            """
        username: str = pk
        current_user: models.PlatformUser = request.user
        # return userinfo if user wants to access own profile
        if username is not None and username == current_user.username:
            instance = current_user
        else:
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request: Request):
        """Gets the requested queryset for users

        Parameters
        ----------
        session : if session argument is set return current user info

        Returns
        -------
        Cards
            list of cards
        """
        self_arg: str = request.query_params.get('session', None)
        _queryset = self.get_queryset()

        current_user: models.PlatformUser = self.request.user
        # needed to evaluate the lazy queryset
        if not _queryset.filter(id=1):
            pass
        if (self_arg is not None and
                self_arg == "self"):
            _queryset = _queryset.filter(
                id=current_user.id)

        serializer = serializers.PlatformUserSerializer(_queryset, many=True)
        return Response(serializer.data)
