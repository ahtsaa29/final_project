from django.urls import path, include
from userdetails.views import PayrollView, IssueView, IssueTypeView, DesignationView, ApplicationView, CompanyView
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'company', CompanyView)
# router.register(r'payroll', PayrollViewSet)
# router.register(r'application', ApplicationViewSet)
# router.register(r'issue', IssueViewSet)
# router.register(r'issuetype', IssueTypeViewSet)
# router.register(r'designation', DesignationViewSet)

urlpatterns = [
    # path('',include(router.urls)),
    path('company/',CompanyView.as_view(), name='company'),
    path('payroll/',PayrollView.as_view(), name='payroll'),
    path('issue/',IssueView.as_view(), name='issue'),
    path('issueType/',IssueTypeView.as_view(), name='issueType'),
    path('designation/',DesignationView.as_view(), name='designation'),
    path('application/',ApplicationView.as_view(), name='application'),

]
