from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .models import Task

from .serializers import TaskSerializer, UserSerializer


class TaskView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        tasks = request.user.tasks

        serializer = TaskSerializer(tasks, many=True)
        
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        data = request.data
        data['user'] = request.user.id

        serializer = TaskSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        task = Task.objects.get(id=pk)

        serializer = TaskSerializer(task)
        
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        data = request.data

        task = Task.objects.get(id=pk)

        serializer = TaskSerializer(task, data=data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request: Request, pk: int) -> Response:
        task = Task.objects.get(id=pk)
        task.delete()

        return Response({'message': 'deleted.'})


class UsersView(APIView):
    
    def get(self, request: Request) -> Response:
        users = User.objects.filter(is_superuser=False)

        serializer = UserSerializer(users, many=True)
        
        return Response(serializer.data)