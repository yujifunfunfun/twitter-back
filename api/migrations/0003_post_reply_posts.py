# Generated by Django 3.2.16 on 2023-12-20 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reply_posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.post'),
        ),
    ]
