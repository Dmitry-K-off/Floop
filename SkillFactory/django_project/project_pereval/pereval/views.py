from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import PerevalAdded
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


@extend_schema(
    responses=PerevalSerializer,
    tags=['tasks'],
    summary='Получить перевал по ID',
    description='Возвращает одну запись перевала и статус модерации.'
)
class SubmitDataDetailView(RetrieveAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer
    lookup_field = 'id'


@extend_schema(
    request=PerevalSerializer,
    responses={
        200: OpenApiResponse(description='Успешное редактирование', examples=[{
            'state': 1,
            'message': 'Запись успешно обновлена'
        }]),
        400: OpenApiResponse(description='Редактирование не выполнено', examples=[{
            'state': 0,
            'message': 'Редактирование запрещено — статус не new'
        }]),
    },
    tags=['tasks'],
    summary='Редактировать перевал',
    description='Редактирует поля перевала, если статус = new. Не изменяются данные пользователя.'
)
class SubmitDataUpdateView(APIView):
    def patch(self, request, id):
        try:
            pereval = PerevalAdded.objects.get(id=id)
        except PerevalAdded.DoesNotExist:
            return Response({"state": 0, "message": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)

        if pereval.status != PerevalAdded.StatusChoices.NEW:
            return Response({"state": 0, "message": "Редактирование запрещено — статус не new"}, status=status.HTTP_400_BAD_REQUEST)

        excluded_fields = ['user']
        update_data = {k: v for k, v in request.data.items() if k not in excluded_fields}

        serializer = PerevalSerializer(pereval, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"state": 1, "message": "Запись успешно обновлена"}, status=status.HTTP_200_OK)
        return Response({"state": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    parameters=[
        OpenApiParameter(name='user__email', type=str, location=OpenApiParameter.QUERY, required=True)
    ],
    responses={200: PerevalSerializer(many=True)},
    tags=['tasks'],
    summary='Список перевалов по email пользователя',
    description='Возвращает все перевалы, отправленные пользователем с указанной почтой.'
)
class SubmitDataListByUserView(ListAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']