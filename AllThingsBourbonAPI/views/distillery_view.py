from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Distillery, BourbonStaff

class DistilleryView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single distillery

        Returns:
            Response -- JSON serialized distillery
        """
        try:
            distillery = Distillery.objects.get(pk=pk)
            serializer = DistillerySerializer(distillery, context={'request': request})
            return Response(serializer.data)
        
        except Distillery.DoesNotExist as ex:
            return Response({'message': 'Distillery does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

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
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        distillery = Distillery()

        try:
            distillery.name = request.data["name"]
            distillery.location = request.data["location"]
            distillery.description = request.data["description"]
            distillery.link_to_site = request.data["link_to_site"]
            distillery.distillery_img = request.data["distillery_img"]
        
        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        distillery.staff_member = staff_member

        try:
            distillery.save()
            serializer = DistillerySerializer(distillery, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({"reason": "You passed some bad data"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a distillery

        Returns:
        Response -- Empty body with 204 status code
        """
        staff_member = BourbonStaff.objects.get(user=request.auth.user)

        distillery = Distillery.objects.get(pk=pk)
        distillery.name = request.data['name']
        distillery.location = request.data['location']
        distillery.description = request.data['description']
        distillery.link_to_site = request.data['link_to_site']
        distillery.distillery_img = request.data['distillery_img']
        distillery.staff_member = staff_member

        distillery.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a distillery

        Returns:
        Response -- Empty body with 204, 404, or 500 status code
        """

        try:
            distillery = Distillery.objects.get(pk=pk)
            distillery.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Distillery.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
