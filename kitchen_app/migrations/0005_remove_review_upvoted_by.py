# Generated by Django 2.2.4 on 2021-03-04 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_app', '0004_auto_20210304_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='upvoted_by',
        ),
    ]
