from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from user_rl.renderers import UserRenderer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from userdetails.models import Company, Payroll, Application, ApplicationType, Designation
from rest_framework import viewsets, serializers
from userdetails.serializers import CompanySerializer, PayrollSerializer, ApplicationTypeSerializer, DesignationSerializer, ApplicationSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CompanySerializer
    def create(self,request, *args, **kwargs):
        company = Company.objects.first()
        if company is not None:
            return Response({"message":"You can not add more than 1 company"})
        data = request.data.copy()
        serializer = self.get_serializer(data= data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers= headers
        )
    from rest_framework.decorators import action
    @action(detail= False)
    def attendance(self,request,pk=None):
      return Response({"message":"ERROR"})
      # try:
      #   hrmsuser = User.objects.get(pk=pk)
      #   print(hrmsuser)
      #   atts = Attendance.objects.filter(hrmsuser= hrmsuser)
      #   atts_serializer = AttendanceSerializer(atts, many=True, context= {'request':request})
      #   return Response(atts_serializer.data)
      # except Exception as e:
      #   print(e)
      #   return Response({'message':e})
# company done nachu

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    # permission_classes = [IsAdminUser]
    # custom permission
    serializer_class = PayrollSerializer
    def create(self,request, *args, **kwargs):
        pass
    def update(self,request, *args, **kwargs):
        pass
    def destroy(self,request, *args, **kwargs):
        pass
    def get(self,request, *args, **kwargs):
        pass




class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAdminUser]
    # custom permission
    serializer_class = ApplicationSerializer



class ApplicationTypeViewSet(viewsets.ModelViewSet):
    queryset = ApplicationType.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ApplicationTypeSerializer



class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = DesignationSerializer