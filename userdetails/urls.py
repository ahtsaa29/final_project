from django.urls import path, include
from userdetails.views import PayrollViewSet, ApplicationTypeViewSet, DesignationViewSet, ApplicationViewSet, CompanyViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'payroll', PayrollViewSet)
router.register(r'application', ApplicationViewSet)
router.register(r'applicationtype', ApplicationTypeViewSet)
router.register(r'designation', DesignationViewSet)

urlpatterns = [
    path('',include(router.urls)),
    # path('company/',CompanyView.as_view(), name='company'),
    # path('payroll/',PayrollView.as_view(), name='payroll'),
    # path('issue/',IssueView.as_view(), name='issue'),
    # path('issueType/',IssueTypeView.as_view(), name='issueType'),
    # path('designation/',DesignationView.as_view(), name='designation'),
    # path('application/',ApplicationView.as_view(), name='application'),

]
