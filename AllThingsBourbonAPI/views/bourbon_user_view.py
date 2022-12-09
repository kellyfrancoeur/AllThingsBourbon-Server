from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import BourbonUser


class BourbonUserView(ViewSet):
    """All Things Bourbon bourbon user view"""

    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """

        users = BourbonUser.objects.all()
        serialized = BourbonUserSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user record
        """

        user = BourbonUser.objects.get(pk=pk)
        serialized = BourbonUserSerializer(user, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a bourbon member

        Returns:
        Response -- Empty body with 204 status code
        """

        user = BourbonUser.objects.get(pk=pk)
        user.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BourbonUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Bourbon User"""
    class Meta:
        model = BourbonUser
        fields = ('id', 'full_name', 'birthday',)