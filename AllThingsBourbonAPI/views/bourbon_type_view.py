"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import BourbonType


class BourbonTypeView(ViewSet):
    """All Things Bourbon bourbon types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single bourbon type

        Returns:
            Response -- JSON serialized bourbon type
        """
        bourbon_type = BourbonType.objects.get(pk=pk)
        serializer = BourbonTypeSerializer(bourbon_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all bourbon types

        Returns:
            Response -- JSON serialized list of bourbon types
        """
        bourbon_types = BourbonType.objects.all()
        serializer = BourbonTypeSerializer(bourbon_types, many=True)
        return Response(serializer.data)

class BourbonTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for bourbon types
    """
    class Meta:
        model = BourbonType
        fields = ('id', 'type',)