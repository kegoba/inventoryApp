# Generated by Django 5.1.5 on 2025-01-15 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='contact_info',
            new_name='email',
        ),
    ]
