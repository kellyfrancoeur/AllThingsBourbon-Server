"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from django.db.models import Case, When, Value, IntegerField, BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Cocktail, CocktailTried, BourbonUser

class CocktailsTriedView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single cocktail tried

        Returns:
            Response -- JSON serialized cocktail tried
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)
        cocktail_tried = CocktailTried.objects.get(pk=pk)

        cocktail_tried.is_cocktail_enthusiast = False

        if cocktail_tried.cocktail_enthusiast == bourbon_user:
            cocktail_tried.is_cocktail_enthusiast = True

        serializer = CocktailsTriedSerializer(cocktail_tried, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all cocktails tried

        Returns:
            Response -- JSON serialized list of cocktails tried
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)

        cocktails_tried = CocktailTried.objects.annotate(
               is_cocktail_enthusiast=Case(
                   When(cocktail_enthusiast=bourbon_user,
                        then=Value(True)),
                   default=Value(False),
                   output_field=BooleanField())) \
                .all()

        if "cocktail" in request.query_params:
            cocktails_tried = CocktailTried.objects.filter(cocktail__id=request.query_params['cocktail'])

        serializer = CocktailsTriedSerializer(cocktails_tried, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized cocktail tried instance
        """
        cocktail_enthusiast = BourbonUser.objects.get(user=request.auth.user)
        cocktail = Cocktail.objects.get(pk=request.data['cocktail'])

        cocktail_tried = CocktailTried.objects.create(
            comments = request.data['comments'],
            rating = request.data['rating'],
            cocktail = cocktail,
            cocktail_enthusiast = cocktail_enthusiast
        ) 

        serialized = CocktailsTriedSerializer(cocktail_tried)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a cocktail tried

        Returns:
        Response -- Empty body with 204 status code
        """
        cocktail = Cocktail.objects.get(pk=pk)

        cocktail_tried = CocktailTried.objects.get(pk=pk)
        cocktail_tried.comments = request.data['comments']
        cocktail_tried.rating = request.data['rating']
        cocktail_tried.cocktail = cocktail

        cocktail_tried.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class BourbonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonUser
        fields = ('id', 'full_name',)

class CocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ('id', 'name', 'ingredients', 'how_to_make', 'cocktail_img', 'type_of_cocktail',)


class CocktailsTriedSerializer(serializers.ModelSerializer):
    """JSON serializer for cocktails tried
    """
    cocktail_enthusiast = BourbonUserSerializer(many=False)
    cocktail = CocktailSerializer(many=False)

    class Meta:
        model = CocktailTried
        fields = ('id', 'cocktail_enthusiast', 'cocktail', 'comments', 'rating',)
        depth = 1