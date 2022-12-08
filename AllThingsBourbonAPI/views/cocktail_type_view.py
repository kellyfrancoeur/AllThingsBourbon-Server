from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import CocktailType


class CocktailTypeView(ViewSet):
    """All Things Bourbon cocktail types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single cocktail type

        Returns:
            Response -- JSON serialized cocktail type
        """
        cocktail_type = CocktailType.objects.get(pk=pk)
        serializer = CocktailTypeSerializer(cocktail_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all cocktail types

        Returns:
            Response -- JSON serialized list of cocktail types
        """
        cocktail_types = CocktailType.objects.all()
        serializer = CocktailTypeSerializer(cocktail_types, many=True)
        return Response(serializer.data)

class CocktailTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for cocktail types
    """
    class Meta:
        model = CocktailType
        fields = ('id', 'type',)