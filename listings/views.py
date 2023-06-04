from django.shortcuts import render
from .serializer import ServiceSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .crypto import password_decode,PasswordManager
from rest_framework.response import Response
from .models import Service as Services
import base64
import json
import zlib
from rest_framework.status import HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST
from rest_framework.decorators import action

class Service(ModelViewSet):

    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return Services.objects.filter(user=self.request.user)
    @action(methods=['POST',],detail=False)
    def password(self,request):

        """
            this part allow us to retrieve the user password 
            it takes as parameter the master password
            then if the master password is correct we return the service password
        """

        if request.user.is_authenticated:

            manager = PasswordManager()
            try:
                master_password = request.data.get('master_password')
                service = request.data.get("process_id")
            except:
                return Response({"error": "Invalid master password"})
            
            
            try:
                is_correct = manager.verify(master_password,request.user.master_password)
            except Exception:
                return Response(status=HTTP_400_BAD_REQUEST,data={"error":"something went wrong"})
            

            if is_correct:

                print(is_correct)
                password_data = Services.objects.get(pk=service).password_hashed
                clear_password_data = zlib.decompress(base64.b64decode(password_data)).decode()
                key = Services.objects.get(pk=service).key
                password_data = json.loads(clear_password_data)
                return Response(status=HTTP_200_OK,data={"password":password_decode(password_data,key)})


            return Response(status=HTTP_401_UNAUTHORIZED,data={"error":"incorrect password"})

        return Response({"error":"user must be authenticated"})
    
    def create(self,request):

        if request.user.is_authenticated:
                
                try:
                    
                    name = request.data.get('name')
                    login = request.data.get("login")
                    password = request.data.get('password')
                    image = request.data.get('image')
                    category = request.data.get('category')
                    score = request.data.get('score')

                    if not all([len(name), len(login), password, image, category,score]):
                        return Response(status=HTTP_400_BAD_REQUEST, data={"status": "false", "message": "One or more fields are missing."})

                    if len(name) <= 4:
                        return Response(status=HTTP_400_BAD_REQUEST, data={"status": "false", "message": "Name should be at least 5 characters long."})

                    # If all values are present and the size of name is greater than 4, continue with the rest of the code here

                    
                    
                except Exception as e:
                    print(e)
                    return Response({"status": "false"})
                
                user = request.user

                try:
                    service = Services.objects.create(service_name=name,password_hashed=password,user=user,login=login,image=image,category=category,score=score)

                except Exception as e:
                    print(e)
                    return Response(status=HTTP_400_BAD_REQUEST,data={"status":"false"})
                

                return Response(status=HTTP_200_OK,data={"status":"true","id":service.id,"service":service.service_name})

        return Response({"error":"user must be authenticated"})
    



        




