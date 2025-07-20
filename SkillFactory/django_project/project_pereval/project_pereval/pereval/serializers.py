from rest_framework import serializers
from .models import User, Coords, PerevalAdded, PerevalImage, PerevalAreas


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'first_name', 'patronymic']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImage
        fields = ['title', 'file']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = PerevalAdded
        fields = [
            'beautytitle', 'title', 'other_titles', 'connect',
            'user', 'coords', 'area',
            'winter_level', 'summer_level', 'autumn_level', 'spring_level',
            'images'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images', [])

        # Проверка существующего пользователя
        user, _ = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
        coords = Coords.objects.create(**coords_data)

        pereval = PerevalAdded.objects.create(
            user=user,
            coords=coords,
            status=PerevalAdded.StatusChoices.NEW,
            **validated_data
        )

        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval, **image_data)

        return pereval
