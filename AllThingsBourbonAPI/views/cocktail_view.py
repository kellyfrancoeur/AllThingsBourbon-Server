from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Cocktail, CocktailType, BourbonUser, BourbonStaff

class CocktailView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single cocktail

        Returns:
            Response -- JSON serialized cocktail
        """
        cocktail = Cocktail.objects.get(pk=pk)
        serializer = CocktailSerializer(cocktail)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all cocktails

        Returns:
            Response -- JSON serialized list of cocktails
        """
        cocktails = Cocktail.objects.all()
        serializer = CocktailSerializer(cocktails, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized cocktail instance
        """
        staff_member = BourbonStaff.objects.get(user=request.auth.user)
        type_of_cocktail = CocktailType.objects.get(pk=request.data['type_of_cocktail'])

        cocktail = Cocktail.objects.create(
            name = request.data['name'],
            ingredients = request.data['ingredients'],
            how_to_make = request.data['how_to_make'],
            cocktail_img = request.data['cocktail_img'],
            type_of_cocktail = type_of_cocktail,
            staff_member = staff_member
        ) 

        serialized = CocktailSerializer(cocktail, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a cocktail

        Returns:
        Response -- Empty body with 204 status code
        """
        type_of_cocktail = CocktailType.objects.get(pk=request.data['type_of_cocktail'])
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        cocktail = Cocktail.objects.get(pk=pk)
        cocktail.name = request.data['name']
        cocktail.ingredients = request.data['ingredients']
        cocktail.how_to_make = request.data['how_to_make']
        cocktail.cocktail_img = request.data['cocktail_img']
        cocktail.type_of_cocktail = type_of_cocktail
        cocktail.staff_member = staff_member

        cocktail.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a cocktail

        Returns:
        Response -- Empty body with 204 status code
        """

        cocktail = Cocktail.objects.get(pk=pk)
        cocktail.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class BourbonStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonStaff
        fields = ('id', 'full_name',)

class CocktailTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailType
        fields = ('id', 'type',)

class CocktailSerializer(serializers.ModelSerializer):
    """JSON serializer for cocktails
    """
    staff_member = BourbonStaffSerializer(many=False)
    type_of_cocktail = CocktailTypeSerializer(many=False)
    class Meta:
        model = Cocktail
        fields = ('id', 'name', 'ingredients', 'how_to_make', 'cocktail_img', 'type_of_cocktail', 'staff_member',)
        depth = 1
