# Generated by Django 5.2.1 on 2025-06-23 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_developer_projects_alter_tag_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='developers', to='project.project'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='tags', to='project.project'),
        ),
    ]
