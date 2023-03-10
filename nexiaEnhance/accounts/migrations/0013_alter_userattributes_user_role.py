# Generated by Django 4.1.3 on 2022-12-01 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_userattributes_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userattributes",
            name="user_role",
            field=models.CharField(
                choices=[
                    ("preparer", "Preparer"),
                    ("reviewer", "Reviewer"),
                    ("ult_resp_auth", "Ultimate responsible authority"),
                    ("nexia_enhance_admin", "Nexia Enhance administrator"),
                    ("IT_admin", "IT administrator"),
                    ("nexia_user", "Nexia user"),
                    ("nexia_superuser", "Nexia superuser"),
                ],
                default="staff",
                max_length=20,
            ),
        ),
    ]
