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
from school_management.util import roleChecker, roleTimer
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
            user = Login.objects.get(email__exact = serializer.data['email'])
            try :
                if pwd_context.verify (serializer.data['password'], user.password):
                    accessToken = jwt.encode({'exp':roleTimer(user.role),'email':user.email, 'role':user.role}, 'secret')
                    f = open('media/'+str(user.image), 'rb')
                    image = File(f)
                    data = base64.b64encode(image.read())
                    f.close()
                    return Response(dict(accessToken=accessToken, name=user.name, role = user.role, image = data), status= status.HTTP_201_CREATED)
                return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)
            except:
                return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
            try:
                authToken = request.headers["auth"]
                payload  = jwt.decode(authToken,"secret")
                role = payload['role']
                serializer  = RegistrationSerializer(data = request.data)
                if serializer.is_valid():
                    if(roleChecker(role,request.data['role'])):
                        loginSerializer = Login(
                                        name = request.data['name'],
                                        email =  request.data['email'],
                                        role = request.data['role'],
                                        image = request.data['image'],
                                        password = pwd_context.encrypt(request.data['password']))
                        loginSerializer.save()
                        return Response(status= status.HTTP_201_CREATED)
                    return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.ExpiredSignatureError:
                return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
            except jwt.exceptions.DecodeError:
                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
            except:
                return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)


    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['Post'])
def register1(request):
    try:
        loginSerializer = Login(
                                    name = 'Amit',
                                    email =  'amitkuntal1998@gmal.com',
                                    role = 'Admin',
                                    image = 'media/profile/aaa.jpg',
                                    password = pwd_context.encrypt('Amit@12345'))
        loginSerializer.save()
        return Response(status= status.HTTP_201_CREATED)
    except:
        return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    def put(self, request):
            try:
                authToken = request.headers["auth"]
                payload  = jwt.decode(authToken,"secret")
                role = payload['role']
                user = Login.objects.get(email__exact = payload['email'])
                userid = user.id
                #If Admin Wants to update there profile picture
                if (role == "Admin"):
                    admin  = Admin.objects.get_or_create(userid = userid)[0]
                    admin.mobile = request.data["mobile"]
                    admin.save()
                    return Response(status= status.HTTP_201_CREATED)
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
                    return Response(status= status.HTTP_201_CREATED)
                #If User role is school employee
                elif (role in ['Accountant', 'Teacher','Reception']):
                    employee = Employee.objects.get_or_create(userid = userid)[0]
                    employee.mobile = request.data["mobile"]
                    employee.classid = request.data["classid"]
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
                    return Response(status= status.HTTP_201_CREATED)
            #Exception Handling
            except jwt.exceptions.ExpiredSignatureError:
                return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
            except jwt.exceptions.DecodeError:
                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
            # except:
            #     return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            user = Login.objects.get(email__exact = payload['email'])
            userid = user.id
            f = open('media/'+str(user.image), 'rb')
            image = File(f)
            data = base64.b64encode(image.read())
            f.close()
            #If user role is admin then admin profile will return
            if (role == "Admin"):
                admin  = Admin.objects.get_or_create(userid = userid)[0]
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=dict(mobile= admin.mobile))
                return Response(response,status= status.HTTP_201_CREATED)
            #If userrole is school then school profile will return
            elif (role == 'School'):
                school = School.objects.get_or_create(userid = userid)[0]
                additionalInfo = dict(address1 =school.address1 ,address2 = school.address2,address3 = school.address3,city = school.city,state = school.state,zip =school.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=additionalInfo)
                return Response(response,status= status.HTTP_201_CREATED)
            #If User role is Employe then Employee profile will return
            elif (role in ['Accountant', 'Teacher','Reception']):
                employee = Employee.objects.get_or_create(userid = userid)[0]
                additionalInfo = dict(fathername = employee.fathername,mothername=employee.mothername,dob = employee.dob,mobile=employee.mobile,address1 =employee.address1 ,address2 = employee.address2,address3 = employee.address3,city = employee.city,state = employee.state,zip =employee.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=additionalInfo)
                return Response(response,status= status.HTTP_201_CREATED)
            #If user role is student then student profile will return
            elif (role == 'Student'):
                student = Student.objects.get_or_create(userid = userid)
                additionalInfo = dict(fathername = student.fathername,mothername=student.mothername,dob = student.dob,mobile=student.mobile,address1 =student.address1 ,address2 = student.address2,address3 = student.address3,city = student.city,state = student.state,zip =student.zip)
                response = dict(personalInfo=dict(name = user.name,email=user.email, image=data),additionalInfo=additionalInfo)
                return Response(dict(personalInfo = user, additionalinfo= student),status= status.HTTP_201_CREATED)
        #Exception Handling
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)
    

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


# class GetCount(APIView):
#     def put(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)



