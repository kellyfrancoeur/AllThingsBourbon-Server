"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Distillery, BourbonUser, BourbonStaff

class DistilleryView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single distillery

        Returns:
            Response -- JSON serialized distillery
        """
        distillery = Distillery.objects.get(pk=pk)
        serializer = DistillerySerializer(distillery)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all distilleries

        Returns:
            Response -- JSON serialized list of distilleries
        """
        distilleries = Distillery.objects.all()
        serializer = DistillerySerializer(distilleries, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized distillery instance
        """

        new_distillery = Distillery()
        new_distillery.staff_member = BourbonStaff.objects.get(user=request.auth.user)
        new_distillery.name = request.data['name']
        new_distillery.location = request.data['location']
        new_distillery.description = request.data['description']
        new_distillery.link_to_site = request.data['link_to_site']
        new_distillery.distillery_img = request.data['distillery_img']
        new_distillery.save()

        serialized = DistillerySerializer(new_distillery, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a distillery

        Returns:
        Response -- Empty body with 204 status code
        """

        distillery = Distillery.objects.get(pk=pk)
        staff_member = BourbonStaff.objects.get(user=request.auth.user)
        distillery.name = request.data['name']
        distillery.location = request.data['location']
        distillery.description = request.data['description']
        distillery.link_to_site = request.data['link_to_site']
        distillery.distillery_img = request.data['distillery_img']
        distillery.staff_member = staff_member

        distillery.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a distillery

        Returns:
        Response -- Empty body with 204 status code
        """

        distillery = Distillery.objects.get(pk=pk)
        distillery.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BourbonStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonStaff
        fields = ('id', 'full_name',)

class DistillerySerializer(serializers.ModelSerializer):
    """JSON serializer for distilleries
    """
    staff_member = BourbonStaffSerializer(many=False)
    class Meta:
        model = Distillery
        fields = ('id', 'name', 'location', 'description', 'link_to_site', 'distillery_img', 'staff_member',)
        depth = 1
