# Generated by Django 4.2.10 on 2024-03-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_pet2_delete_pet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=100)),
                ('race', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('health', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('hair', models.CharField(max_length=100)),
                ('description', models.CharField(default='none', max_length=255)),
            ],
        ),
    ]
