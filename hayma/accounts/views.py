from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminUserDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk):
        try:
            User.objects.get(pk=pk).delete()
            return Response(status=204)
        except User.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

    def post(self, request, pk):
        action = request.data.get('action')
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
        if action == 'block':
            user.is_blocked = True
            user.save()
        elif action == 'unblock':
            user.is_blocked = False
            user.save()
        else:
            return Response({'detail': 'Invalid action'}, status=400)
        return Response(UserSerializer(user).data)

# Create your views here.
