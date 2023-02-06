from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from user_rl.serializers import HrmsUserLoginSerializer,HrmsUserRegistrationSerializer,HrmsUserProfileSerializer,HrmsUserChangePasswordSerializer,AttendanceSerializer,SendPasswordResetEmailSerializer,HrmsUserPasswordResetSerializer
from django.contrib.auth import authenticate
from user_rl.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from datetime import datetime
from django.shortcuts import render
# from face_recog.face_recognition import face_identify as fc
import cv2, numpy, os

from user_rl.models import Attendance



def get_tokens_for_user(hrmsuser):
    refresh = RefreshToken.for_user(hrmsuser)
    time_stamp = datetime.now()
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'time_stamp':str(time_stamp)
    }

def register_dataset(hrmsuser):
  face_cap = cv2.CascadeClassifier('face_recognition/haarcascade_frontalface_default.xml')
  datasets = 'face_recognition/datasets/'  
  video_cap = cv2.VideoCapture(0)
  size = 4
  path = os.path.join(datasets, hrmsuser)
  if not os.path.isdir(path):
    os.mkdir(path)
  (width, height) = (130, 100)   
  count = 0
  while count < 30: 
      (_, cap_data) = video_cap.read()
      col = cv2.cvtColor(cap_data, cv2.COLOR_BGR2GRAY)
      faces = face_cap.detectMultiScale(col, 1.3, 4)
      for (x, y, w, h) in faces:
          cv2.rectangle(cap_data, (x, y), (x + w, y + h), (255, 0, 0), 2)
          face = col[y:y + h, x:x + w]
          face_resize = cv2.resize(face, (width, height))
          cv2.imwrite('% s/% s.png' % (path, count), face_resize)
      count += 1
      
      cv2.imshow('Reading your image', cap_data)
      if cv2.waitKey(100) == ord("z"):
          break

  return Response({
      'message': "Your face is stored for future Logins"
  }, status=status.HTTP_200_OK)

class HrmsUserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]
    def post(self, request,format=None):
        serializer = HrmsUserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hrmsuser = serializer.save()
        token = get_tokens_for_user(hrmsuser)
        face_dataset = register_dataset(hrmsuser)
        data ={'dataset':face_dataset,'token': token,'message':'registration success','location':'register_dataset'}
        return Response(data, status= status.HTTP_201_CREATED)
        


class HrmsUserLoginView(APIView):
    renderer_classes = [UserRenderer]
    # @action(detail= False)
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
    serializer = HrmsUserProfileSerializer(request.user)
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


# class HrmsUserDelete(APIView):
#   renderer_classes = [UserRenderer]
#   # permission_classes = [IsAdminUser]
#   def destroy(self, request, *args, **kwargs):
#     instance = self.get_object()
#     self.perform_destroy(instance)
#     return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
  
