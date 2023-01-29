from rest_framework import serializers
from userdetails.models import Company,Designation, Payroll, ApplicationType, Application


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    company_id = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields= "__all__"

class DesignationSerializer (serializers.HyperlinkedModelSerializer):
    designation_id = serializers.ReadOnlyField()

    class Meta:
        model = Designation
        fields= "__all__"


class PayrollSerializer (serializers.HyperlinkedModelSerializer):
    payroll_id = serializers.ReadOnlyField()
    class Meta:
        model = Payroll
        fields= "__all__"
        read_only_fields =['salary','tax_amount','gross_salary','net_salary']


class ApplicationTypeSerializer (serializers.HyperlinkedModelSerializer):
    Applicationtype_id = serializers.ReadOnlyField()
    
    class Meta:
        model = ApplicationType
        fields= "__all__"


class ApplicationSerializer (serializers.HyperlinkedModelSerializer):
    Application_id = serializers.ReadOnlyField()

    class Meta:
        model = Application
        fields= "__all__"