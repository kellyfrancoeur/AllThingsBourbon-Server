from django.http import HttpResponseServerError
from django.db.models import Case, When, Value, IntegerField, BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Distillery, DistilleryVisited, BourbonUser

class DistilleriesVisitedView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single distillery visited

        Returns:
            Response -- JSON serialized distillery visited
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)
        distillery_visited = DistilleryVisited.objects.get(pk=pk)

        distillery_visited.is_distillery_enthusiast = False

        if distillery_visited.distillery_enthusiast == bourbon_user:
            distillery_visited.is_distillery_enthusiast = True

        serializer = DistilleriesVisitedSerializer(distillery_visited, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all distilleries visited

        Returns:
            Response -- JSON serialized list of distilleries visited
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)
        distilleries_visited = DistilleryVisited.objects.filter(distillery_enthusiast=bourbon_user)

        serializer = DistilleriesVisitedSerializer(distilleries_visited, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized distillery visited instance
        """
        distillery_enthusiast = BourbonUser.objects.get(user=request.auth.user)
        distillery = Distillery.objects.get(pk=request.data['distillery'])

        distillery_visited = DistilleryVisited.objects.create(
            comments = request.data['comments'],
            rating = request.data['rating'],
            distillery = distillery,
            distillery_enthusiast = distillery_enthusiast
        ) 

        serialized = DistilleriesVisitedSerializer(distillery_visited)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a distillery visited

        Returns:
        Response -- Empty body with 204 status code
        """
        distillery = Distillery.objects.get(pk=request.data['distillery'])

        distillery_visited = DistilleryVisited.objects.get(pk=pk)
        distillery_visited.comments = request.data['comments']
        distillery_visited.rating = request.data['rating']
        distillery_visited.distillery = distillery

        distillery_visited.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a distillery visited

        Returns:
        Response -- Empty body with 204 status code
        """

        distillery_visited = DistilleryVisited.objects.get(pk=pk)
        distillery_visited.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class BourbonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonUser
        fields = ('id', 'full_name',)

class DistillerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Distillery
        fields = ('id', 'name', 'location', 'description', 'link_to_site', 'distillery_img',)


class DistilleriesVisitedSerializer(serializers.ModelSerializer):
    """JSON serializer for distillerys visited
    """
    distillery_enthusiast = BourbonUserSerializer(many=False)
    distillery = DistillerySerializer(many=False)

    class Meta:
        model = DistilleryVisited
        fields = ('id', 'distillery_enthusiast', 'distillery', 'comments', 'rating',)
        depth = 1