# Generated by Django 4.1.3 on 2022-12-21 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("riskregister", "0004_riskregister_03_qualityrisk_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="riskregister_03_qualityrisk", name="firm_name",
        ),
        migrations.RemoveField(
            model_name="riskregister_04_riskresponse", name="firm_name",
        ),
    ]
