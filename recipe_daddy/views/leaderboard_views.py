from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from recipe_daddy.models.user_models import User
from recipe_daddy.serializers.leaderboard_serializers import LeaderboardSerializer


class LeaderboardViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all().order_by("-food_saved")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
