# Generated by Django 4.2.10 on 2024-03-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0008_animal_animal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='age',
            field=models.FloatField(),
        ),
    ]
