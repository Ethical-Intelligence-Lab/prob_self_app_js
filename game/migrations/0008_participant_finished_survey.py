# Generated by Django 3.1.5 on 2021-12-11 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_remove_participant_submitted_demographics'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='finished_survey',
            field=models.BooleanField(default=False),
        ),
    ]
