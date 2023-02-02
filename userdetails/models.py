from django.db import models
from datetime import datetime

# Create your models here.


class Company(models.Model):
    # done
    company_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=50, null=False)
    phone = models.BigIntegerField(null=False)
    email = models.EmailField(null=False)
    address = models.CharField(max_length=100, null=False)
    logo = models.ImageField(upload_to='uploads/logo', height_field=None, width_field=None, max_length=100, null=True)
    pan_no = models.BigIntegerField(null=False)
    added_date = models.DateTimeField(default=datetime.now, editable=False)

class Designation(models.Model):
    # admin
    designation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, unique=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2,default=0, null=False)

    def __str__(self):
        return self.name
        
class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    designation =models.ForeignKey(Designation, on_delete=models.CASCADE, default=None)
    salary = models.DecimalField(max_digits=8, decimal_places=2,default=0, null=False)
    gross_salary = models.DecimalField(max_digits=8, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=8, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2)
    overtime = models.DecimalField(max_digits=8, decimal_places=2)
    allowance = models.DecimalField(max_digits=8, decimal_places=2)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    medical_claim = models.DecimalField(max_digits=8, decimal_places=2)
    net_salary = models.FloatField()
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
    name = models.CharField(max_length=25, null=False)

    def __str__(self):
        return self.name

class Application(models.Model):
    # user le pathaune
    application_id = models.AutoField(primary_key=True)
    apply_for = models.ForeignKey(ApplicationType, on_delete=models.CASCADE, default=None, null=False)
    title = models.CharField(max_length=25, null=False)
    reason = models.TextField(null=False)
    date = models.DateTimeField(default=datetime.now, editable=False)
    for_days = models.IntegerField(null=False)
    STATUS = (
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Pending','Pending')
    )

