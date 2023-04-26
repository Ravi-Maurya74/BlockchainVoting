from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def custom_validate_email(value):
    if value.split("@")[1]!="iiitl.ac.in":
        raise ValidationError('This domain is not allowed')

# Create your models here.


class Election(models.Model):
    title = models.CharField(max_length=300)
    number_of_choices = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    running = models.BooleanField(default=True)
    number_of_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title


class Choice(models.Model):
    name = models.CharField(max_length=200)
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="choices"
    )
    choice_id = models.IntegerField()

    class Meta:
        ordering = ["choice_id"]

    def __str__(self) -> str:
        return self.name


class Voter(models.Model):
    name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True,validators=[
        custom_validate_email
    ])
    password = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(8, "This field must contain atleast 8 characters.")
        ],
    )
    admin = models.BooleanField(default=False)
    voted_in = models.ManyToManyField(
        Election,
        related_name="voters",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name
