from django.http import HttpResponseServerError
from rest_framework.decorators import action
from django.db.models import Case, When, Value, IntegerField, BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Bourbon, BourbonTried, BourbonUser, Descriptor, BourbonDescriptor

class BourbonsTriedView(ViewSet):
    
    def retrieve(self, request, pk):
        """Handle GET requests for single bourbon tried

        Returns:
            Response -- JSON serialized bourbon tried
        """
        bourbon_user = BourbonUser.objects.get(user=request.auth.user)
        tried = BourbonTried.objects.get(pk=pk)

        tried.is_bourbon_enthusiast = False

        if tried.bourbon_enthusiast == bourbon_user:
            tried.is_bourbon_enthusiast = True

        serializer = BourbonsTriedSerializer(tried, context={'request': request})
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

        descriptors = request.data["descriptors"]
        for descriptor in descriptors:
            try:
                descriptor_to_assign = Descriptor.objects.get(pk=descriptor)
            except Descriptor.DoesNotExist:
                    return Response({"message": "Descriptor does not exist"}, status = status.HTTP_404_NOT_FOUND)

        tried = BourbonTried.objects.create(
            comments = request.data['comments'],
            rating = request.data['rating'],
            bourbon = bourbon,
            bourbon_enthusiast = bourbon_enthusiast
        ) 

        for descriptor in descriptors:
            descriptor_to_assign = Descriptor.objects.get(pk=descriptor)
            tried_descriptor = BourbonDescriptor()
            tried_descriptor.bourbon_tried = tried
            tried_descriptor.descriptor = descriptor_to_assign
            tried_descriptor.save()

        serialized = BourbonsTriedSerializer(tried)
        return Response({'message': 'Bourbon has been added!'}, serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a bourbon tried

        Returns:
        Response -- Empty body with 204 status code
        """
        bourbon = Bourbon.objects.get(pk=pk)

        tried = BourbonTried.objects.get(pk=pk)
        tried.comments = request.data['comments']
        tried.rating = request.data['rating']
        tried.bourbon = bourbon
        tried.descriptors.set(request.data["descriptors"])
        tried.save()

        return Response({'message': 'Bourbon has been updated!'}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a bourbon tried

        Returns:
        Response -- Empty body with 204 status code
        """

        bourbon_tried = BourbonTried.objects.get(pk=pk)
        bourbon_tried.delete()

        return Response({'message': 'Bourbon has been removed'}, status=status.HTTP_204_NO_CONTENT)

class BourbonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BourbonUser
        fields = ('id', 'full_name',)

class BourbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bourbon
        fields = ('id', 'name',)

class BourbonDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descriptor
        fields = ('id', 'label',)


class BourbonsTriedSerializer(serializers.ModelSerializer):
    """JSON serializer for bourbons tried
    """
    bourbon_enthusiast = BourbonUserSerializer(many=False)
    bourbon = BourbonSerializer(many=False)
    descriptors = BourbonDescriptorSerializer(many=True)

    class Meta:
        model = BourbonTried
        fields = ('id', 'bourbon_enthusiast', 'bourbon', 'comments', 'rating', 'descriptors',)
        depth = 1