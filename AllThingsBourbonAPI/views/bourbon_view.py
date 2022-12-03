"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Bourbon, BourbonType, BourbonStaff

class BourbonView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single bourbon

        Returns:
            Response -- JSON serialized bourbon
        """
        bourbon = Bourbon.objects.get(pk=pk)
        serializer = BourbonSerializer(bourbon)
        return Response(serializer.data)

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
        type_of_bourbon = BourbonType.objects.get(pk=request.data['type_of_bourbon'])

        bourbon = Bourbon.objects.create(
            name = request.data['name'],
            proof = request.data['proof'],
            aroma = request.data['aroma'],
            taste = request.data['taste'],
            finish = request.data['finish'],
            description = request.data['description'],
            made_in = request.data['made_in'],
            link_to_buy = request.data['link_to_buy'],
            bourbon_img = request.data['bourbon_img'],
            type_of_bourbon = type_of_bourbon,
            staff_member = staff_member
        ) 

        serialized = BourbonSerializer(bourbon, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a bourbon

        Returns:
        Response -- Empty body with 204 status code
        """
        type_of_bourbon = BourbonType.objects.get(pk=request.data['type_of_bourbon'])
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        bourbon = Bourbon.objects.get(pk=pk)
        bourbon.name = request.data['name']
        bourbon.proof = request.data['proof']
        bourbon.aroma = request.data['aroma']
        bourbon.taste = request.data['taste']
        bourbon.finish = request.data['finish']
        bourbon.description = request.data['description']
        bourbon.made_in = request.data['made_in']
        bourbon.link_to_buy = request.data['link_to_buy']
        bourbon.bourbon_img = request.data['bourbon_img']
        bourbon.type_of_bourbon = type_of_bourbon
        bourbon.staff_member = staff_member

        bourbon.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a bourbon

        Returns:
        Response -- Empty body with 204 status code
        """

        bourbon = Bourbon.objects.get(pk=pk)
        bourbon.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
