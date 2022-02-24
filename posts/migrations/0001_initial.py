# Generated by Django 3.2.8 on 2022-02-20 17:05

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('comment_count', models.IntegerField(blank=True, default=0, null=True)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('vote_rank', models.IntegerField(blank=True, default=0, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PostReact',
            fields=[
                ('value', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike')], max_length=20)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.ManyToManyField(blank=True, related_name='app_user', through='posts.PostReact', to=settings.AUTH_USER_MODEL),
        ),
    ]