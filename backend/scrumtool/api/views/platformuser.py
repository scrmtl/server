from rest_framework import viewsets

from . import models
from . import serializers
from rest_framework.response import Response


class PlatformUserViewSet(viewsets.ModelViewSet):
    queryset = models.PlatformUser.objects.all()

    def get_queryset(self):
        if 'task_pk' not in self.kwargs:
            return self.queryset
        else:
            return self.queryset.filter(task_cards=self.kwargs['task_pk'])
    serializer_class = serializers.PlattformUserSerializer

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

    def list(self, request, lane_pk=None):
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
        if not _queryset:
            pass
        if (self_arg is not None and
                self_arg == "self"):
            _queryset = _queryset.filter(
                id=current_user.id)

        serializer = serializers.PlattformUserSerializer(_queryset, many=True)
        return Response(serializer.data)
