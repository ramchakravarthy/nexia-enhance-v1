# Generated by Django 4.1.3 on 2022-11-29 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_firm_is_active_user_user_role"),
    ]

    operations = [
        migrations.DeleteModel(name="User",),
    ]
