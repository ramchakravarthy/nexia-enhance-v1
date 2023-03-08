# Generated by Django 4.1.3 on 2023-03-02 12:35

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ("riskreg", "0017_alter_rca_contributory_cause_1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_1_reviewer_comments",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Reviewer comments"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_2",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Second contributory cause"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_2_reviewer_comments",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Reviewer comments"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_3",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Third contributory cause"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="contributory_cause_3_reviewer_comments",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Reviewer comments"
            ),
        ),
        migrations.AlterField(
            model_name="rca",
            name="immediate_cause_reviewer_comments",
            field=django_quill.fields.QuillField(
                blank=True, null=True, verbose_name="Reviewer comments"
            ),
        ),
    ]