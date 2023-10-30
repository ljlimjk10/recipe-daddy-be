from rest_framework import serializers
from recipe_daddy.models.user_models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "food_saved", "password", "food_saved_goal"]
        extra_kwargs = {"password":{"write_only":True}, "food_saved": {"read_only": True}}
    
    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data['password']
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self,instance,validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.food_saved = validated_data.get("food_saved", instance.food_saved)
        instance.food_saved_goal = validated_data.get("food_saved_goal", instance.food_saved_goal)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance
