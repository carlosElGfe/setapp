# Generated by Django 3.2.6 on 2022-05-27 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0014_auto_20220519_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id_ciclo', models.AutoField(primary_key=True, serialize=False)),
                ('subciclos', models.CharField(default='', max_length=590)),
                ('subfechas', models.CharField(default='', max_length=590)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('id_refeer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.refeer')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]