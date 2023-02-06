from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)





class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)


class ApplicationTypeViewSet(viewsets.ModelViewSet):
    queryset = ApplicationType.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ApplicationTypeSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = DesignationSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Succesfully deleted item"},status=status.HTTP_204_NO_CONTENT)