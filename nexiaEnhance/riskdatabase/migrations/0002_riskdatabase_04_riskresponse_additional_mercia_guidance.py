# Generated by Django 4.1.3 on 2022-12-19 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("riskdatabase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="riskdatabase_04_riskresponse",
            name="additional_mercia_guidance",
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
