from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    last_name  = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    height = models.IntegerField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.height}m"


class PerevalAreas(models.Model):
    id_parent = models.BigIntegerField()
    title = models.TextField()

    def __str__(self):
        return self.title


class PerevalAdded(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'new', 'Новый'
        PENDING = 'pending', 'В работе'
        ACCEPTED = 'accepted', 'Принят'
        REJECTED = 'rejected', 'Отклонён'

    beautytitle = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    other_titles = models.TextField(blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    winter_level = models.CharField(max_length=10, blank=True, null=True)
    summer_level = models.CharField(max_length=10, blank=True, null=True)
    autumn_level = models.CharField(max_length=10, blank=True, null=True)
    spring_level = models.CharField(max_length=10, blank=True, null=True)
    area = models.ForeignKey(PerevalAreas, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded, related_name="images", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.ImageField(upload_to='pereval_images/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Фото {self.id}"

