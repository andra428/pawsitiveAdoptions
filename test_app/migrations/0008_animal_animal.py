# Generated by Django 4.2.10 on 2024-03-16 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0007_animal_adopted_animal_gender_animal_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='animal',
            field=models.CharField(default='Dog', max_length=100),
        ),
    ]
