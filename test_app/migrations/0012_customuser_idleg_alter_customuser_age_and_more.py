# Generated by Django 4.2.10 on 2024-03-26 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0011_remove_customuser_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='idleg',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='animal',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='hair',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='race',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='size',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
