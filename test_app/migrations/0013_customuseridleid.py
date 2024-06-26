# Generated by Django 4.2.10 on 2024-04-13 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0012_customuser_idleg_alter_customuser_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserIdleId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.animal')),
            ],
            options={
                'unique_together': {('customuser', 'idle')},
            },
        ),
    ]
