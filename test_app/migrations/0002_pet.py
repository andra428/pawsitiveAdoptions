# Generated by Django 4.2.10 on 2024-03-05 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=255)),
                ('race', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('health', models.CharField(max_length=255)),
            ],
        ),
    ]
