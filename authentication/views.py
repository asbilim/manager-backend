from .serializer import AccountSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_400_BAD_REQUEST

class AccountViewset(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        
        if self.action == 'create':
            permissions = []
        elif self.action == 'change':
            permissions = [IsAuthenticated]
        else :
            permissions = [IsAdminUser]

        return [permission() for permission in permissions]

    def create(self,request):
        
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if email is not None and username is not None and password is not None:
            try:
                user = get_user_model().objects.create(email=email,username=username,password=password)
            except:
                return Response(status=HTTP_400_BAD_REQUEST,data={"status":"error","message":"username or email taken"})
            if user:
                return Response(status=HTTP_201_CREATED,data={"status":"success"})
            
            return Response(status=HTTP_400_BAD_REQUEST,data={"status":"error"})
        
        return Response(status=HTTP_400_BAD_REQUEST,data={"status":"error"})
    
    @action(detail=False,methods=['POST',])
    def change(self,request):
        
        master_password = request.data.get("master_password")
        try:
            user = request.user
            user.master_password = master_password
            user.changed = 0
            user.save()
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST,data={"status":"error"})
    
        return Response(status=HTTP_201_CREATED,data={"status":"success"})

        

