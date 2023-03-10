# Generated by Django 4.1.3 on 2022-11-29 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Firm",
            fields=[
                ("firm_id", models.AutoField(primary_key=True, serialize=False)),
                ("firm_name", models.CharField(max_length=200)),
                ("firm_domain", models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="firm_name",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.firm",
            ),
            preserve_default=False,
        ),
    ]
