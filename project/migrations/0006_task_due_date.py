# Generated by Django 5.2.1 on 2025-06-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
