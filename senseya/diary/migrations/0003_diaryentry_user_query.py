# Generated by Django 5.1.3 on 2024-12-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_diaryentry_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='user_query',
            field=models.TextField(blank=True, null=True),
        ),
    ]
