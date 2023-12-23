# Generated by Django 3.2.16 on 2023-12-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_post_reply_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reply_posts',
        ),
        migrations.AddField(
            model_name='post',
            name='reply_posts',
            field=models.ManyToManyField(blank=True, related_name='_api_post_reply_posts_+', to='api.Post'),
        ),
    ]