from django.db import models
from datetime import datetime


# Create your models here.


class Company(models.Model):
    # admin
    company_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='uploads/logo', height_field=None, width_field=None, max_length=100, null=True)
    pan_no = models.BigIntegerField()
    added_date = models.DateTimeField(default=datetime.now, editable=False)

class Designation(models.Model):
    # admin
    designation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    salary = models.DecimalField(max_digits=8, decimal_places=2,default=0)

    def __str__(self):
        return self.name
        
class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    designation =models.ForeignKey(Designation, on_delete=models.CASCADE, default=None)
    salary = models.DecimalField(max_digits=6, decimal_places=2,default=None)
    gross_salary = models.DecimalField(max_digits=8, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=8, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2)
    overtime = models.DecimalField(max_digits=8, decimal_places=2)
    allowance = models.DecimalField(max_digits=8, decimal_places=2)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    medical_claim = models.DecimalField(max_digits=8, decimal_places=2)
    net_salary = models.FloatField()
    # hrmsuser = models.OneToOneField(HrmsUser,on_delete=models.CASCADE, default=None)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)

    def save(self, *args, **kwargs):
        self.salary = self.designation.salary
        self.gross_salary = self.designation.salary + self.overtime + self.allowance + self.bonus + self.medical_claim
        self.tax_amount = (self.gross_salary * self.tax_percent)/100
        self.net_salary = self.gross_salary - self.tax_amount

    def __str__(self):
        return self.designation.name + "-" + self.salary
    
class ApplicationType(models.Model):
    issue_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Application(models.Model):
    # user le pathaune
    application_id = models.AutoField(primary_key=True)
    apply_for = models.ForeignKey(ApplicationType, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=25)
    reason = models.TextField()
    date = models.DateTimeField(default=datetime.now, editable=False)
    for_days = models.IntegerField()
    STATUS = (
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Pending','Pending')
    )

