from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Location
from .serializers import LocationSerializer


class PublicLocationView(APIView):
    def get(self, request):
        # user 필터 제거하여 모든 위치 정보 가져오기
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)


class LocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk, user=self.request.user)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            # 현재 로그인한 유저의 이름 정보 추가
            validated_data = serializer.validated_data
            validated_data['first_name'] = request.user.first_name
            validated_data['last_name'] = request.user.last_name
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            location = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
