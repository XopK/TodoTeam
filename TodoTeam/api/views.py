from rest_framework.decorators import api_view
from rest_framework.response import Response
from task.models import Task
from .serializers import TaskSerializer

@api_view(['GET'])
def getTask(request):
    task = Task.objects.all()
    serializer = TaskSerializer(task, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createTask(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)