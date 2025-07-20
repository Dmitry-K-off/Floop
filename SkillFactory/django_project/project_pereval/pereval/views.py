# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import PerevalSerializer


@extend_schema(
    request=PerevalSerializer,
    responses={201: PerevalSerializer},
    tags=['tasks'],
    summary='Добавить новый перевал',
    description='Принимает данные перевала и пользователя, сохраняет в базе. Устанавливает статус new.'
)
class SubmitDataView(APIView):
    def post(self, request, format=None):
        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            pereval = serializer.save()
            return Response(PerevalSerializer(pereval).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
