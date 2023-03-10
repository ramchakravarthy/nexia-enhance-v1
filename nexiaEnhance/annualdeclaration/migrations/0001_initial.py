# Generated by Django 4.1.3 on 2023-02-08 17:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnnualDeclaration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "evaluation_year",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(2500),
                            django.core.validators.MinValueValidator(2022),
                        ]
                    ),
                ),
                ("evaluation_date", models.DateField(auto_now=True)),
                ("previous_evaluation_date", models.DateField()),
                ("evaluation_1", models.BooleanField()),
                ("evaluation_2", models.BooleanField()),
                ("evaluation_3", models.BooleanField()),
                ("conclusion_1", models.BooleanField()),
                ("conclusion_2", models.BooleanField()),
                ("conclusion_3", models.BooleanField()),
                ("actions_and_communications_1", models.BooleanField()),
                (
                    "actions_and_communications_1_b",
                    models.TextField(blank=True, max_length=10000, null=True),
                ),
                ("actions_and_communications_2", models.BooleanField()),
                ("actions_and_communications_3", models.BooleanField()),
                ("individual", models.CharField(max_length=500)),
                ("signature_date", models.DateField(auto_now=True)),
            ],
        ),
    ]
