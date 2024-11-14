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


class LocationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk, user=self.request.user)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET 요청 추가
    def get(self, request, pk):
        location = self.get_object(pk)
        if isinstance(location, Response):  # get_object가 Response일 경우
            return location
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def delete(self, request, pk):
        location = self.get_object(pk)
        if isinstance(location, Response):  # get_object가 Response일 경우
            return location
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        location = self.get_object(pk)
        if isinstance(location, Response):  # get_object가 Response일 경우
            return location
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            location = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 로그인한 사용자의 모든 위치 조회
        locations = self.get_queryset()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # 로그인한 사용자의 위치 필터링
        return Location.objects.filter(user=self.request.user)

    def post(self, request):
        # 새로운 위치 생성
        data = request.data.copy()  # request.data를 복사하여 수정 가능하게 만듭니다.
        data["first_name"] = request.user.first_name
        data["last_name"] = request.user.last_name

        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 로그인한 사용자 정보 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
