# Generated by Django 4.1.3 on 2023-03-02 12:32

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ("riskreg", "0016_alter_rca_identified_deficiency_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_1",
            field=django_quill.fields.QuillField(
                verbose_name="First contributory cause"
            ),
        ),
    ]
