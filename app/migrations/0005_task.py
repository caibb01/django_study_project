# Generated by Django 4.1.7 on 2023-04-21 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lever', models.SmallIntegerField(choices=[('2', '严重'), ('3', '临时'), ('1', '紧急')], default=1, verbose_name='级别')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(max_length=64, verbose_name='信息')),
                ('processor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.admin', verbose_name='负责人')),
            ],
        ),
    ]