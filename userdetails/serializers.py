from rest_framework import serializers
from userdetails.models import Company,Designation, Payroll, IssueType, Application, Issue


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields= "__all__"

    def validate_phone(self, value):
        if value < 9000000000 or value > 9999999999:
            raise serializers.ValidationError('wrong format')
        return value


class DesignationSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Designation
        fields= "__all__"


class PayrollSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payroll
        fields= "__all__"
        read_only_fields =['salary','tax_amount','gross_salary','net_salary']


class IssueTypeSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IssueType
        fields= "__all__"


class ApplicationSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields= "__all__"


class IssueSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields= "__all__"