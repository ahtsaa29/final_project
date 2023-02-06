# Generated by Django 4.1.5 on 2023-02-02 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userdetails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('pan_no', models.BigIntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identified', models.BooleanField(default=False)),
                ('designation', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='userdetails.designation')),
                ('payroll', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='userdetails.payroll')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(default=None)),
                ('is_late', models.BooleanField()),
                ('is_early', models.BooleanField()),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
