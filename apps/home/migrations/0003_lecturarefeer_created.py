# Generated by Django 3.2.6 on 2022-05-04 20:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220504_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturarefeer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
