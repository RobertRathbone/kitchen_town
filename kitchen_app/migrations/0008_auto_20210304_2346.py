# Generated by Django 2.2.4 on 2021-03-04 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_app', '0007_auto_20210304_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='upvoted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_upvote', to='kitchen_app.User'),
        ),
    ]
