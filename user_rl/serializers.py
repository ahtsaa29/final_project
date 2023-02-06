from rest_framework import serializers
from user_rl.models import User, Attendance
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from user_rl.utils import Util
from rest_framework.response import Response
# from face_recog.face_recognition import face_store



class HrmsUserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['email','name','password','password2',]
        read_only_fields = ('is_active', 'is_staff','user_id')

        # fields = ['email','name','password','password2','faces']
        extra_kwargs ={
            'password':{'write_only': True}
        }
      
    def validate_phone(self, value):
        if value < 9000000000 or value > 9999999999:
            raise serializers.ValidationError('wrong format')
        return value
    # validate pw
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        # return super().validate(attrs)
        return attrs

    def create(self, validate_data):
        # faces= face_store('name')
        # return HrmsUser.objects.create_user(faces,**validate_data)
        return User.objects.create_user(**validate_data)

class HrmsUserLoginSerializer(serializers.ModelSerializer):
  # time_stamp = serializers.SerializerMethodField()
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password','identified']

  # def get_time_stamp(obj):
  #   print(obj)
  #   return obj.last_login

class HrmsUserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class AttendanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attendance
    fields = ['id', 'email', 'name']


class HrmsUserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      hrmsuser = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(hrmsuser.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(hrmsuser)
      print('Password Reset Token', token)
      link = 'http://127.0.0.1:8000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':hrmsuser.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class HrmsUserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      hrmsuser = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(hrmsuser, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      hrmsuser.set_password(password)
      hrmsuser.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(hrmsuser, token)
      raise serializers.ValidationError('Token is not Valid or Expired')



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'