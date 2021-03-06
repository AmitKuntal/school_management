from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['userid', 'address1', 'address2' , 'address3', 'city', 'state', 'zip']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['userid', 'mobile']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = ['classid','schoolid', 'feename', 'cycle' , 'amount'] 

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id','schoolid', 'classname', 'section']

class FeeDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDeposit
        fields = ['userid', 'feestructureid', 'depositdate' , 'depositamount']

class AddHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['classid','teacherid', 'homework', 'homeworkdate', 'image']        

class TranferCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferCertificate
        fields = ['userid', 'requestedby', 'approveby' , 'requesteddate', 'approvedate', 'status']        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    def create(self, validated_data):
        return LoginPayload(**validated_data)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['name', 'email', 'role' , 'image', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['name', 'email', 'role' , 'image','active','id']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class AddSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subjectname','classid']

class AddEducationPortal(serializers.ModelSerializer):
    class Meta:
        model = EducationPortal
        fields = ['subjectid','chaptername', 'videolink']

class EducationPortalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationPortal
        fields = '__all__'

class AddEmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = ['userid', 'attendancedate','status']

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = '__all__'
        
class ErrorMessageSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=80)
    message =  serializers.CharField(max_length=80)
    def create(self, validated_data):
        return ErrorMessage(**validated_data)
    

class LoginResponseSerializer(serializers.Serializer):
    accessToken  = serializers.CharField(max_length=1000)
    refreshToken = serializers.CharField(max_length=1000)
    
    def create(self, validated_data):
        return LoginResponse(**validated_data)
    