# Generated by Django 3.1.5 on 2021-11-29 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_demographics_edu'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='elapsed_sec',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='finish_dt',
            field=models.DateTimeField(null=True),
        ),
    ]
