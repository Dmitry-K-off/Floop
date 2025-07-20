from ..models import User, Coords, PerevalAdded, PerevalImage


class SubmitDataService:
    @staticmethod
    def get_or_create_user(data: dict) -> User:
        user, _ = User.objects.get_or_create(
            email=data['email'],
            defaults={
                'phone': data.get('phone'),
                'last_name': data.get('last_name'),
                'first_name': data.get('first_name'),
                'patronymic': data.get('patronymic'),
            }
        )
        return user

    @staticmethod
    def create_coords(data: dict) -> Coords:
        return Coords.objects.create(
            latitude=data['latitude'],
            longitude=data['longitude'],
            height=data['height'],
        )

    @staticmethod
    def create_pereval(data: dict, user: User, coords: Coords) -> PerevalAdded:
        return PerevalAdded.objects.create(
            user=user,
            coords=coords,
            beautytitle=data.get('beautytitle'),
            title=data['title'],
            other_titles=data.get('other_titles'),
            connect=data.get('connect'),
            area=data['area'],
            winter_level=data.get('winter_level'),
            summer_level=data.get('summer_level'),
            autumn_level=data.get('autumn_level'),
            spring_level=data.get('spring_level'),
            status=PerevalAdded.StatusChoices.NEW,
        )

    @staticmethod
    def attach_images(pereval: PerevalAdded, images: list) -> None:
        for img_data in images:
            PerevalImage.objects.create(
                pereval=pereval,
                title=img_data.get('title'),
                file=img_data['file'],
            )
