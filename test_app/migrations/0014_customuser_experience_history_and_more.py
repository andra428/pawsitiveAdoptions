# Generated by Django 4.2.10 on 2024-05-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0013_customuseridleid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='experience_history',
            field=models.CharField(default='experienta/istoric', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='housing_environment',
            field=models.CharField(default='mediu de gazduire', max_length=300, null=True),
        ),
    ]
