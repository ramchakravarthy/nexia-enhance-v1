# Generated by Django 4.1.3 on 2023-01-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("riskreg", "0005_rca"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rca",
            name="is_pervasive",
            field=models.BooleanField(
                default=False, verbose_name="Is the deficiency pervasive?"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="is_pervasive_comments",
            field=models.TextField(
                verbose_name="If noted to be pervasive, please provide more information."
            ),
        ),
    ]