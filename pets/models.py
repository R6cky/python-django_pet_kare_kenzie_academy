from django.db import models


class SetSex(models.TextChoices):
    MALE = "Male",
    FEMALE = "Female",
    NOT_FORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SetSex.choices, default=SetSex.NOT_FORMED)

    group = models.ForeignKey("groups.Group", on_delete=models.PROTECT, related_name="pets")
    traits = models.ManyToManyField("traits.Trait", related_name="pets")