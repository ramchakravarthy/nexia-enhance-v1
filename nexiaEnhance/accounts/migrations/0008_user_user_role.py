# Generated by Django 4.1.3 on 2022-11-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_remove_user_firm_name_remove_user_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_role",
            field=models.CharField(
                choices=[
                    ("staff", "Staff"),
                    ("reviewer", "Reviewer"),
                    ("ult_resp", "Ultimate responsibility"),
                    ("admin", "Nexia Enhance administrator"),
                    ("IT_admin", "IT administrator"),
                ],
                default="staff",
                max_length=20,
            ),
        ),
    ]
