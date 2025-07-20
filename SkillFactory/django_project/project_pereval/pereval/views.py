from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import PerevalSerializer
from .services.submit_data_service import SubmitDataService


@extend_schema(
    request=PerevalSerializer,
    responses={201: PerevalSerializer},
    tags=['tasks'],
    summary='Добавить новый перевал',
    description='Создаёт перевал и связанные объекты: координаты, пользователя, фото. Устанавливает статус "new".'
)
class SubmitDataView(APIView):
    def post(self, request, format=None):
        serializer = PerevalSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user_data = validated_data.pop('user')
            coords_data = validated_data.pop('coords')
            images_data = validated_data.pop('images', [])

            user = SubmitDataService.get_or_create_user(user_data)
            coords = SubmitDataService.create_coords(coords_data)
            pereval = SubmitDataService.create_pereval(validated_data, user, coords)
            SubmitDataService.attach_images(pereval, images_data)

            response_data = PerevalSerializer(pereval).data
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
