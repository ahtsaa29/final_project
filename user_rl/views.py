from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_rl.serializers import HrmsUserLoginSerializer,HrmsUserRegistrationSerializer,HrmsUserProfileSerializer,HrmsUserChangePasswordSerializer,SendPasswordResetEmailSerializer,HrmsUserPasswordResetSerializer
from django.contrib.auth import authenticate
from user_rl.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from face_recog.face_recognition import face_identify as fc
# Create your views here.



def get_tokens_for_user(hrmsuser):
    refresh = RefreshToken.for_user(hrmsuser)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class HrmsUserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        serializer = HrmsUserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hrmsuser = serializer.save()
        token = get_tokens_for_user(hrmsuser)
        return Response({'token': token,'message':'registration success'}, status= status.HTTP_201_CREATED)


class HrmsUserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        serializer = HrmsUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        # face_identify = fc.face_identify('name')
        user = authenticate(email=email, password=password, identified= True)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token,'message':'login success'}, status= status.HTTP_201_CREATED)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class HrmsUserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = HrmsUserProfileSerializer(request.hrmsuser)
    return Response(serializer.data, status=status.HTTP_200_OK)



class HrmsUserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = HrmsUserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class HrmsUserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = HrmsUserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset Successfully'}, status=status.HTTP_200_OK)