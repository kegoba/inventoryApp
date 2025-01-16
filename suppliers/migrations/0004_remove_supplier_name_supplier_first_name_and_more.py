# Generated by Django 5.1.5 on 2025-01-15 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0003_alter_supplier_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='name',
        ),
        migrations.AddField(
            model_name='supplier',
            name='first_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='supplier',
            name='last_name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
