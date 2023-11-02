from recipe_daddy.models.user_models import User
from recipe_daddy.serializers.user_serializers import UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import mixins,generics
from recipe_daddy.permissions import OwnerOrNoAccessToUser

class UserViewSet(generics.GenericAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return []
        else:
            return [OwnerOrNoAccessToUser()]

    def get_object(self):
        username = self.request.query_params.get("username")
        email = self.request.query_params.get("email")

        if username:
            obj = get_object_or_404(self.queryset, username=username)
        elif email:
            obj = get_object_or_404(self.queryset, email=email)
        else:
            obj = get_object_or_404(self.queryset, pk=self.request.user.id)

        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)