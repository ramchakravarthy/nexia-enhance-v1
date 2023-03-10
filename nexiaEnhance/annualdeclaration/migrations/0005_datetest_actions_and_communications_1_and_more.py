# Generated by Django 4.1.3 on 2023-02-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annualdeclaration", "0004_datetest_evaluation_date_datetest_evaluation_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="datetest",
            name="actions_and_communications_1",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="actions_and_communications_1_b",
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name="datetest",
            name="actions_and_communications_2",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="actions_and_communications_3",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="conclusion_1",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="conclusion_2",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="conclusion_3",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="evaluation_1",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="evaluation_2",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="evaluation_3",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="individual",
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="datetest",
            name="signature_date",
            field=models.DateField(auto_now=True),
        ),
    ]
