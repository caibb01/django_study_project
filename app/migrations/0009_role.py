# Generated by Django 4.1.7 on 2023-03-06 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
    ]
