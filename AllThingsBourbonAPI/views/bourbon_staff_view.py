from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from AllThingsBourbonAPI.models import BourbonStaff


class BourbonStaffView(ViewSet):
    """All Things Bourbon bourbon staff view"""

    def list(self, request):
        """Handle GET requests to get all staff members

        Returns:
            Response -- JSON serialized list of staff members
        """

        staffs = BourbonStaff.objects.all()
        serialized = BourbonStaffSerializer(staffs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single staff member

        Returns:
            Response -- JSON serialized staff member record
        """

        staff = BourbonStaff.objects.get(pk=pk)
        serialized = BourbonStaffSerializer(staff, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class BourbonStaffSerializer(serializers.ModelSerializer):
    """JSON serializer for Bourbon Staff"""
    class Meta:
        model = BourbonStaff
        fields = ('id', 'full_name', 'bio',)