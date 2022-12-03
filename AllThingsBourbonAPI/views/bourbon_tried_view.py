"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from django.db.models import Case, When, Value, IntegerField, BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Bourbon, BourbonTried, BourbonUser, Descriptor

class BourbonsTriedView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single bourbon tried

        Returns:
            Response -- JSON serialized bourbon tried
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)
        bourbon_tried = BourbonTried.objects.get(pk=pk)

        bourbon_tried.is_bourbon_enthusiast = False

        if bourbon_tried.bourbon_enthusiast == bourbon_user:
            bourbon_tried.is_bourbon_enthusiast = True

        serializer = BourbonsTriedSerializer(bourbon_tried, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all bourbons tried

        Returns:
            Response -- JSON serialized list of bourbons tried
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)

        bourbons_tried = BourbonTried.objects.annotate(
               is_bourbon_enthusiast=Case(
                   When(bourbon_enthusiast=bourbon_user,
                        then=Value(True)),
                   default=Value(False),
                   output_field=BooleanField())) \
                .all()

        if "bourbon" in request.query_params:
            bourbons_tried = BourbonTried.objects.filter(bourbon__id=request.query_params['bourbon'])

        serializer = BourbonsTriedSerializer(bourbons_tried, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized bourbon tried instance
        """
        bourbon_enthusiast = BourbonUser.objects.get(user=request.auth.user)
        bourbon = Bourbon.objects.get(pk=request.data['bourbon'])

        bourbon_tried = BourbonTried.objects.create(
            comments = request.data['comments'],
            rating = request.data['rating'],
            bourbon = bourbon,
            bourbon_enthusiast = bourbon_enthusiast
        ) 

        serialized = BourbonsTriedSerializer(bourbon_tried)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a bourbon tried

        Returns:
        Response -- Empty body with 204 status code
        """
        bourbon = Bourbon.objects.get(pk=pk)

        bourbon_tried = BourbonTried.objects.get(pk=pk)
        bourbon_tried.comments = request.data['comments']
        bourbon_tried.rating = request.data['rating']
        bourbon_tried.bourbon = bourbon

        bourbon_tried.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post', 'delete'], detail=True)
    def bourbondescriptor(self, request, pk=None):
        """Managing bourbon descriptors"""
        bourbon_tried = BourbonTried.objects.get(pk=pk)
        if request.method == "POST":
            descriptor = Descriptor.objects.get(pk=request.data["descriptorId"])
            bourbon_tried.descriptors.add(descriptor)
            return Response({"Descriptor has been added"}, status=status.HTTP_204_NO_CONTENT)
        elif request.method == "DELETE":
            descriptor = Descriptor.objects.get(pk=request.data["descriptorId"])
            bourbon_tried.descriptors.remove(descriptor)
            return Response({"Descriptor has been removed"}, status=status.HTTP_204_NO_CONTENT)

class BourbonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonUser
        fields = ('id', 'full_name',)

class BourbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bourbon
        fields = ('id', 'name', 'proof', 'aroma', 'taste', 'finish', 'description', 'made_in', 'bourbon_img', 'type_of_bourbon')


class BourbonsTriedSerializer(serializers.ModelSerializer):
    """JSON serializer for bourbons tried
    """
    bourbon_enthusiast = BourbonUserSerializer(many=False)
    bourbon = BourbonSerializer(many=False)

    class Meta:
        model = BourbonTried
        fields = ('id', 'bourbon_enthusiast', 'bourbon', 'comments', 'rating', 'descriptors',)
        depth = 1