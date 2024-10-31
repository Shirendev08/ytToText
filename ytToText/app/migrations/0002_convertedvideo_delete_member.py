# Generated by Django 5.1.2 on 2024-10-31 01:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField()),
                ('converted_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='converted_videos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Converted Video',
                'verbose_name_plural': 'Converted Videos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]