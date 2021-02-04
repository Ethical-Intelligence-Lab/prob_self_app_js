# Generated by Django 3.1.5 on 2021-02-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('load_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('worker_id', models.CharField(max_length=100)),
                ('assignment_id', models.CharField(max_length=100)),
                ('hit_id', models.CharField(max_length=100)),
                ('game_type', models.CharField(max_length=50)),
            ],
        ),
    ]
