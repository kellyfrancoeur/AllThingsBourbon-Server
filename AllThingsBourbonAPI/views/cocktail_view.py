from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Cocktail, CocktailType, BourbonStaff

class CocktailView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single cocktail

        Returns:
            Response -- JSON serialized cocktail
        """
        try:
            cocktail = Cocktail.objects.get(pk=pk)
            serializer = CocktailSerializer(cocktail, context={'request': request})
            return Response(serializer.data)
        
        except Cocktail.DoesNotExist as ex:
            return Response({'message': 'Cocktail does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

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

        cocktail = Cocktail()

        try:
            cocktail.name = request.data["name"]
            cocktail.ingredients = request.data["ingredients"]
            cocktail.how_to_make = request.data["how_to_make"]
            cocktail.cocktail_img = request.data["cocktail_img"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        cocktail.staff_member = staff_member

        try:
            type = CocktailType.objects.get(pk=request.data["type_of_cocktail"])
            cocktail.type_of_cocktail = type
        
        except CocktailType.DoesNotExist as ex:
            return Response({'message': 'Cocktail type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cocktail.save()
            serializer = CocktailSerializer(cocktail, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a cocktail

        Returns:
        Response -- Empty body with 204 status code
        """

        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        cocktail = Cocktail.objects.get(pk=pk)
        cocktail.name = request.data["name"]
        cocktail.ingredients = request.data["ingredients"]
        cocktail.how_to_make = request.data["how_to_make"]
        cocktail.cocktail_img = request.data["cocktail_img"]
        cocktail.staff_member = staff_member

        try:
            type = CocktailType.objects.get(pk=request.data["type_of_cocktail"])
            cocktail.type_of_cocktail = type

            cocktail.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a cocktail

        Returns:
        Response -- Empty body with 204, 404, or 500 status code
        """

        try:
            cocktail = Cocktail.objects.get(pk=pk)
            cocktail.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Cocktail.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
