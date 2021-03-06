from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import *
from .serializers import *
import uuid
from passlib.context import CryptContext
import jwt
import datetime
from school_management.util import *
from django.core.files import File
import base64


pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

#class Based view for login
class LoginView(APIView):
    def post(self, request):
        serializer  = LoginSerializer(data = request.data)
        if serializer.is_valid():
            try :
                user = Login.objects.get(email__exact = serializer.data['email'])
                if serializer.data['password'] == user.password:
                    if(user.active):
                        accessToken = jwt.encode({'exp':roleTimer(user.role),'email':user.email, 'role':user.role}, 'secret')
                        image = user.image
                        data = base64.b64encode(image)
                        return Response(dict(accessToken=accessToken, name=user.name, role = user.role, image = data), status= status.HTTP_201_CREATED)
                    return Response(dict(code="Failed", message = "Your Account is locked"))
                return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)
            except Login.DoesNotExist:
                return Response( dict(code="Failed", message ="You don't have any account"), status = status.HTTP_401_UNAUTHORIZED)
            except:
                return Response( dict(code="Failed", message ="Something went wrong"), status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



# Create your views here.
class RegisterView(APIView):
    def put(self, request):
            try:
                authToken = request.headers["auth"]
                payload  = jwt.decode(authToken,"secret")
                role = payload['role']
                serializer  = RegistrationSerializer(data = request.data)
                if serializer.is_valid():
                    if(roleChecker(role,request.data['role']) and request.data['role'] != 'Student'):
                        loginSerializer = Login(
                                        name = request.data['name'],
                                        email =  request.data['email'],
                                        role = request.data['role'],
                                        image = resizeImage(request.data['image']),
                                        password =request.data['password'])
                        loginSerializer.save()
                        return Response(status= status.HTTP_201_CREATED)
                    return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.ExpiredSignatureError:
                return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
            except jwt.exceptions.DecodeError:
                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
            except:
                return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView1(APIView):
    def post(self, request):
        serializer  = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            loginSerializer = Login(
                            name = request.data['name'],
                            email =  request.data['email'],
                            role = request.data['role'],
                            image = request.data['image'].file.read(),
                            password =request.data['password'])
            loginSerializer.save()
            return Response(status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProfileView(APIView):
    def put(self, request):
            try:
                authToken = request.headers["auth"]
                payload  = jwt.decode(authToken,"secret")
                role = payload['role']
                user = Login.objects.get(email__exact = payload['email'])
                user.email =  request.data["email"]
                user.name =  request.data["name"]
                user.save()
                userid = user.id
                #If Admin Wants to update there profile picture
                if (role == "Admin"):
                    admin  = Admin.objects.get_or_create(userid = userid)[0]
                    admin.mobile = request.data["mobile"]
                    admin.save()
                      #If Schools wants to update there profile picture
                elif (role == 'School'):
                    school = School.objects.get_or_create(userid = userid)[0]
                    school.address1 =  request.data["address1"]
                    school.address2 =  request.data["address2"]
                    school.address3 =  request.data["address3"]
                    school.city =  request.data["city"]
                    school.state =  request.data["state"]
                    school.zip =  request.data["zip"]
                    school.save()
                     #If User role is school employee
                elif (role in ['Accountant', 'Teacher','Reception']):
                    employee = Employee.objects.get_or_create(userid = userid)[0]
                    employee.mobile = request.data["mobile"]
                    employee.dob = request.data["dob"]
                    employee.fathername = request.data["fathername"]
                    employee.mothername = request.data["mothername"]
                    employee.address1 = request.data["address1"]
                    employee.address2 = request.data["address2"]
                    employee.address3 = request.data["address3"]
                    employee.city = request.data["city"]
                    employee.state = request.data["state"]
                    employee.zip = request.data["zip"]
                    employee.save()
                return Response(dict(code="200", message="Profile Updated"), status= status.HTTP_201_CREATED)
            #Exception Handling
            except jwt.exceptions.ExpiredSignatureError:
                return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
            except jwt.exceptions.DecodeError:
                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
            except:
                return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            user = Login.objects.get(email__exact = payload['email'])
            userid = user.id
            data = base64.b64encode(user.image)
            #If user role is admin then admin profile will return
            if (role == "Admin"):
                admin  = Admin.objects.get_or_create(userid = userid)[0]
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=dict(mobile= admin.mobile))
                return Response(response,status= status.HTTP_201_CREATED)
            #If userrole is school then school profile will return
            elif (role == 'School'):
                school = School.objects.get_or_create(userid = userid)[0]
                additionalInfo = dict(address1 =school.address1 ,address2 = school.address2,address3 = school.address3,city = school.city,state = school.state,zip =school.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data, id = userid),additionalInfo=additionalInfo)
                return Response(response,status= status.HTTP_201_CREATED)
            #If User role is Employe then Employee profile will return
            elif (role in ['Accountant', 'Teacher','Reception']):
                employee = Employee.objects.get_or_create(userid = userid)[0]
                additionalInfo = dict(fathername = employee.fathername,mothername=employee.mothername,dob = employee.dob,mobile=employee.mobile,address1 =employee.address1 ,address2 = employee.address2,address3 = employee.address3,city = employee.city,state = employee.state,zip =employee.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=additionalInfo)
                return Response(response,status= status.HTTP_201_CREATED)
            #If user role is student then student profile will return
            elif (role == 'Student'):
                student = Student.objects.get_or_create(userid = userid)[0]
                additionalInfo = dict(fathername = student.fathername,mothername=student.mothername,dob = student.dob,mobileno1=student.mobileno1,mobileno2=student.mobileno2,address1 =student.address1 ,address2 = student.address2,address3 = student.address3,city = student.city,state = student.state,zip =student.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=additionalInfo)
                return Response(response,status= status.HTTP_201_CREATED)
        #Exception Handling
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="500", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetCountView(APIView):
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, name='all'):
        if(name.upper() == 'ALL'):
            school = Login.objects.filter(role='School').all()
            student = Login.objects.filter(role= 'Student').all()
            employee = Login.objects.filter(role__in = ['Teacher','Accountant','Reception'])
            return Response(dict(school=len(school), student = len(student), employee = len(employee)),status=status.HTTP_200_OK)
        elif(name.upper() == 'STUDENT'):
            student = Login.objects.filter(role= 'Student').all()
            return Response(dict(student = len(student)), status=status.HTTP_200_OK)
        elif(name.upper() == 'SCHOOL'):
            school = Login.objects.filter(role='School').all()
            return Response(dict(school = len(school)), status=status.HTTP_200_OK)
        elif(name.upper() == 'TEACHER'):
            student = Login.objects.filter(role= 'Teacher').all()
            return Response(dict(student = len(student)), status=status.HTTP_200_OK)
        elif(name.upper() == 'EMPLOYEE'):
            employee = Login.objects.filter(role__in = ['Teacher','Accountant','Reception'])
            return Response(dict(student = len(student)), status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


#Student Registration API for admin only
class RegisterStudentAdminView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            serializer  = RegistrationSerializer(data = request.data['profile'])
            if serializer.is_valid():
                if(roleChecker(role,request.data['role'])):
                    loginSerializer = Login(
                                    name = request.data['name'],
                                    email =  request.data['email'],
                                    role = request.data['role'],
                                    image = request.data['image'],
                                    password = pwd_context.encrypt(request.data['password']))
                    loginSerializer.save()
                    student = StudentSerializer(data = request.data['additionalInfo'])
                    data = request.data['additionalInfo']
                    if(student.is_valid):
                        studentSerializer = Student(
                                            userid = loginSerializer.id, 
                                            address1 = data['address1'],
                                            address2 = data['address2'],
                                            address3 = data['address3'],
                                            city = data['city'],
                                            state = data['state'],
                                            zip = data['zip'],
                                            schoolid = data['schoolid'],
                                            classid = data['classid'],
                                            fathername = data['fathername'],
                                            mothername = data['mothername'],
                                            mobileno1= data['mobileno1'],
                                            mobileno2=data['mobileno2'],
                                            addmissiondate = data['addmissiondate'],
                                            srno=data['srno'],
                                            promotedclassid = data['promotedclassid'])
                        studentSerializer.save()
                        return Response(status= status.HTTP_201_CREATED)
                    return Response(student.errors, status= status.HTTP_400_BAD_REQUEST)
                return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went Token"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetSchoolsView(APIView):
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            schools =  Login.objects.filter(role ='School').all()
            schoolSerializer =  UserSerializer(schools, many = True)
            schoolsData = schoolSerializer.data
            for school in schoolsData:
                school['image'] = readFiles(school['image'])
            return Response(schoolsData, status = status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class ActivateUserAccount(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            active =  request. data['active']
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            user =  Login.objects.get(email__exact = email)
            user.active = active
            user.save()
            return Response(status = status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Login.DoesNotExist:
            return Response(dict(code="400", message="Could Not find account"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something Went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class CheckToken(APIView):
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            user =  Login.objects.get(email__exact = payload["email"])
            if(user.active):
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Account blocked"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Login.DoesNotExist:
            return Response(dict(code="400", message="Could Not find account"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteStudentView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if (payload["role"] == 'School'):
                Login.objects.filter(id__exact = request.data["id"]).delete()
                Student.objects.filter(userid__exact = request.data["id"]).delete()
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized Request"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Login.DoesNotExist:
            return Response(dict(code="400", message="Could Not find account"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something Went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteEmployeeView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if (payload["role"] == 'School'):
                Login.objects.filter(id__exact = request.data["id"]).delete()
                Employee.objects.filter(userid__exact = request.data["id"]).delete()
                TimeTable.objects.filter(teacherid__exact = request.data["id"]).delete()
                EmployeeAttendance.objects.filter(userid__exact = request.data["id"]).delete()
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized Request"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Login.DoesNotExist:
            return Response(dict(code="400", message="Could Not find account"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteVideoView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if (payload["role"] == 'School'):
                EducationPortal.objects.filter(id__exact = request.data["id"]).delete()
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized Request"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteSubjectView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if (payload["role"] == 'School'):
                Subject.objects.filter(id__exact = request.data["id"]).delete()
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized Request"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteClassView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if (payload["role"] == 'School'):
                Class.objects.filter(id__exact = request.data["id"]).delete()
                Subject.objects.filter(classid__exact = request.data["id"]).delete()
                return Response(dict(passed= "pass"),status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized Request"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

