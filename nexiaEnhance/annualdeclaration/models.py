from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.

class AnnualDeclaration(models.Model):
    # Dates
    evaluation_year = models.IntegerField(validators=[
        MaxValueValidator(2500),
        MinValueValidator(2022)
    ], unique=False)

    evaluation_date = models.DateField(auto_now=True)
    previous_evaluation_date = models.DateField()

    # Evaluations
    evaluation_1 = models.BooleanField()
    evaluation_2 = models.BooleanField()
    evaluation_3 = models.BooleanField()

    # Conclusions
    conclusion_1 = models.BooleanField()
    conclusion_2 = models.BooleanField()
    conclusion_3 = models.BooleanField()

    # Actions and communications
    actions_and_communications_1 = models.BooleanField()
    actions_and_communications_1_b = models.TextField(max_length=10000, unique=False, null=True, blank=True)
    actions_and_communications_2 = models.BooleanField()
    actions_and_communications_3 = models.BooleanField()

    # Declaration
    individual = models.CharField(max_length=500, unique=False)
    signature_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.evaluation_year)

    def get_absolute_url(self):
        return reverse("annual_declaration:view-declaration")

class OLD_AnnualDeclaration(models.Model):
    evaluation_year = models.IntegerField(validators=[
        MaxValueValidator(2500),
        MinValueValidator(2022)
    ], unique=False)

    evaluation_date = models.DateField(auto_now=True)
    previous_evaluation_date = models.DateField()

    # Evaluations
    evaluation_1 = models.BooleanField()
    evaluation_2 = models.BooleanField()
    evaluation_3 = models.BooleanField()

    # Conclusions
    conclusion_1 = models.BooleanField()
    conclusion_2 = models.BooleanField()
    conclusion_3 = models.BooleanField()

    # Actions and communications
    actions_and_communications_1 = models.BooleanField()
    actions_and_communications_1_b = models.TextField(max_length=10000,unique=False,null=True, blank=True)
    actions_and_communications_2 = models.BooleanField()
    actions_and_communications_3 = models.BooleanField()

    # Declaration
    individual = models.CharField(max_length=500, unique=False)
    signature_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.evaluation_year)

    def get_absolute_url(self):
        return reverse("annual_declaration:view-declaration")