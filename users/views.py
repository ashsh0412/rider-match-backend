import jwt
from django.conf import settings
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer, TinyUserSerializer
from rest_framework.exceptions import ParseError, NotFound
from users.models import User
import requests


class Me(APIView):  # receiving logged in user info or edit it

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            raise Response(serializer.errors)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Users(APIView):  # create user

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required")

        serializer = PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data, status=201)  # Created
        else:
            return Response(serializer.errors, status=400)  # Bad Request


class PublicUser(APIView):  # search another user
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = TinyUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            return Response(status=status.HTTP_200_OK)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError("Username and password are required.")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"ok": "Welcome"}, status=200)
        else:
            return Response({"error": "Invalid username or password"}, status=401)


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Log Out"})


# 만약에  대비해서
class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GoogleLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")

            # 구글 OAuth2 토큰을 요청
            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "code": code,
                },
            )

            token_json = token_response.json()
            access_token = token_json.get("access_token")

            # 구글 사용자 정보 가져오기
            user_data_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_data = user_data_response.json()

            # 이메일과 이름을 사용하여 유저 검색 (로그인)
            try:
                user = User.objects.get(username=user_data.get("name"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # 새 사용자 생성
                user = User.objects.create(
                    email=user_data.get("email"),
                    username=user_data.get("name"),  # 구글에서 제공하는 이름
                    first_name=user_data.get("given_name"),
                    last_name=user_data.get("family_name"),
                )
                user.set_unusable_password()  # 비밀번호를 사용할 수 없도록 설정
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            token_response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_CLIENT_ID,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
            )

            token_json = token_response.json()
            access_token = token_json.get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(
                    email=kakao_account.get("email"), username=profile.get("nickname")
                )
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    first_name=kakao_account.get("name"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
