# Generated by Django 4.1.7 on 2023-04-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lever',
            field=models.SmallIntegerField(choices=[('1', '紧急'), ('2', '严重'), ('3', '临时')], default=1, verbose_name='级别'),
        ),
    ]
