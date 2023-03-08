# Generated by Django 4.1.3 on 2022-11-30 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_user_user_role"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="user_role",),
        migrations.CreateModel(
            name="UserAttributes",
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
                    "user_role",
                    models.CharField(
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
                (
                    "profile_pic",
                    models.ImageField(blank=True, upload_to="profile_pics"),
                ),
                (
                    "firm_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.firm"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
    ]