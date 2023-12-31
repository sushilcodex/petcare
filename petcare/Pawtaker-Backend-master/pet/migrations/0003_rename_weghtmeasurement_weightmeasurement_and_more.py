# Generated by Django 4.1.6 on 2023-08-16 10:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("pet", "0002_petmediafile_weghtmeasurement_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="WeghtMeasurement",
            new_name="WeightMeasurement",
        ),
        migrations.RemoveField(
            model_name="petprofile",
            name="pet_breed",
        ),
        migrations.AddField(
            model_name="petbreed",
            name="show_mixed_breeds",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name="petprofile",
            name="primary_breed",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="primary",
                to="pet.petbreed",
            ),
        ),
        migrations.AddField(
            model_name="petprofile",
            name="secondary_breed",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="secondary",
                to="pet.petbreed",
            ),
        ),
        migrations.AlterField(
            model_name="petmediafile",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="File ID",
            ),
        ),
    ]
