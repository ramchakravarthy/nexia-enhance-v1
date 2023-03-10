# Generated by Django 4.1.3 on 2023-01-25 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("riskreg", "0004_alter_riskregister_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="RCA",
            fields=[
                (
                    "identified_deficiency_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("identified_deficiency", models.TextField()),
                ("immediate_cause", models.TextField()),
                (
                    "immediate_cause_reviewer_comments",
                    models.TextField(blank=True, null=True),
                ),
                ("contributory_cause_1", models.TextField()),
                (
                    "contributory_cause_1_reviewer_comments",
                    models.TextField(blank=True, null=True),
                ),
                ("contributory_cause_2", models.TextField(blank=True, null=True)),
                (
                    "contributory_cause_2_reviewer_comments",
                    models.TextField(blank=True, null=True),
                ),
                ("contributory_cause_3", models.TextField(blank=True, null=True)),
                (
                    "contributory_cause_3_reviewer_comments",
                    models.TextField(blank=True, null=True),
                ),
                ("root_cause", models.TextField()),
                ("root_cause_reviewer_comments", models.TextField()),
                ("is_severe", models.BooleanField(default=False)),
                ("is_severe_comments", models.TextField()),
                ("is_pervasive", models.BooleanField(default=False)),
                ("is_pervasive_comments", models.TextField()),
                ("proposed_remedial_action", models.TextField()),
                (
                    "proposed_remedial_action_reviewer_comments",
                    models.TextField(blank=True, null=True),
                ),
                (
                    "proposed_remedial_action_status",
                    models.CharField(
                        choices=[
                            ("not_started", "Not Started"),
                            ("in_progress", "In progress"),
                            ("implemented", "Implemented"),
                        ],
                        max_length=256,
                    ),
                ),
                ("remedial_action_conclusion", models.TextField()),
                ("remedial_action_change", models.TextField()),
                ("preparer_signature", models.CharField(max_length=1000)),
                ("preparer_signature_date", models.DateField(auto_now=True)),
                (
                    "quality_management_head_signature",
                    models.CharField(max_length=1000),
                ),
                (
                    "quality_management_head_signature_date",
                    models.DateField(auto_now=True),
                ),
                ("old_risk_response", models.TextField()),
                ("new_risk_response", models.TextField()),
                (
                    "risk_response",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="root_cause_analysis",
                        to="riskreg.riskregister",
                    ),
                ),
            ],
        ),
    ]
