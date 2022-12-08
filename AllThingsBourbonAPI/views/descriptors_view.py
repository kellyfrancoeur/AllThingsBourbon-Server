from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import Descriptor


class DescriptorView(ViewSet):
    """All Things Bourbon descriptors view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single descriptor

        Returns:
            Response -- JSON serialized descriptor
        """
        descriptor = Descriptor.objects.get(pk=pk)
        serializer = DescriptorSerializer(descriptor)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all descriptors

        Returns:
            Response -- JSON serialized list of descriptors
        """
        descriptors = Descriptor.objects.all()
        serializer = DescriptorSerializer(descriptors, many=True)
        return Response(serializer.data)

class DescriptorSerializer(serializers.ModelSerializer):
    """JSON serializer for descriptors
    """
    class Meta:
        model = Descriptor
        fields = ('id', 'label',)