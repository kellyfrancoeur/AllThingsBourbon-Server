from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Bourbon, BourbonType, BourbonStaff

class BourbonView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single bourbon

        Returns:
            Response -- JSON serialized bourbon instance
        """
        try:
            bourbon = Bourbon.objects.get(pk=pk)
            serializer = BourbonSerializer(bourbon, context={'request': request})
            return Response(serializer.data)
        
        except Bourbon.DoesNotExist as ex:
            return Response({'message': 'Bourbon does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex) 

    def list(self, request):
        """Handle GET requests to get all bourbons

        Returns:
            Response -- JSON serialized list of bourbons
        """
        bourbons = Bourbon.objects.all()
        serializer = BourbonSerializer(bourbons, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized bourbon instance
        """
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        bourbon = Bourbon()

        try:
            bourbon.name = request.data["name"]
            bourbon.proof = request.data["proof"]
            bourbon.aroma = request.data["aroma"]
            bourbon.taste = request.data["taste"]
            bourbon.finish = request.data["finish"]
            bourbon.description = request.data["description"]
            bourbon.made_in = request.data["made_in"]
            bourbon.link_to_buy = request.data["link_to_buy"]
            bourbon.bourbon_img = request.data["bourbon_img"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        bourbon.staff_member = staff_member

        try:
            type = BourbonType.objects.get(pk=request.data["type_of_bourbon"])
            bourbon.type_of_bourbon = type
        
        except BourbonType.DoesNotExist as ex:
            return Response({'message': 'Bourbon type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            bourbon.save()
            serializer = BourbonSerializer(bourbon, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a bourbon

        Returns:
        Response -- Empty body with 204 status code
        """
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        bourbon = Bourbon.objects.get(pk=pk)
        bourbon.name = request.data["name"]
        bourbon.proof = request.data["proof"]
        bourbon.aroma = request.data["aroma"]
        bourbon.taste = request.data["taste"]
        bourbon.finish = request.data["finish"]
        bourbon.description = request.data["description"]
        bourbon.made_in = request.data["made_in"]
        bourbon.link_to_buy = request.data["link_to_buy"]
        bourbon.bourbon_img = request.data["bourbon_img"]
        bourbon.staff_member = staff_member

        try:
            type = BourbonType.objects.get(pk=request.data["type_of_bourbon"])
            bourbon.type_of_bourbon = type

            bourbon.save()
        
        except ValueError:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a bourbon

        Returns:
        Response -- Empty body with 204, 404, 500 status code
        """
        try:
            bourbon = Bourbon.objects.get(pk=pk)
            bourbon.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Bourbon.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BourbonStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonStaff
        fields = ('id', 'full_name',)

class BourbonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonType
        fields = ('id', 'type',)

class BourbonSerializer(serializers.ModelSerializer):
    """JSON serializer for bourbons
    """
    staff_member = BourbonStaffSerializer(many=False)
    type_of_bourbon = BourbonTypeSerializer(many=False)
    class Meta:
        model = Bourbon
        fields = ('id', 'name', 'proof', 'aroma', 'taste', 'finish', 'description', 'made_in', 'link_to_buy', 'bourbon_img', 'type_of_bourbon', 'staff_member',)
        depth = 1
