from recipe_daddy.models.user_models import User
from recipe_daddy.serializers.user_serializers import UserSerializer
from rest_framework import mixins,generics
from rest_framework.permissions import IsAuthenticated
from recipe_daddy.permissions import OwnerOrNoAccessToUser

class UserList(generics.GenericAPIView,
               mixins.ListModelMixin,    
               mixins.CreateModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetails(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = [IsAuthenticated,OwnerOrNoAccessToUser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)