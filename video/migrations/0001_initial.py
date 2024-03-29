# Generated by Django 3.2 on 2021-04-21 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('subscribers', models.CharField(default='0', max_length=10)),
                ('image', models.ImageField(default='default.png', upload_to='channel_pics')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description1', models.CharField(max_length=3000)),
                ('description2', models.CharField(max_length=3000)),
                ('views', models.CharField(default='0', max_length=10)),
                ('likes', models.CharField(default='0', max_length=10)),
                ('dislikes', models.CharField(default='0', max_length=10)),
                ('datePosted', models.DateField(auto_now_add=True)),
                ('thumbnail', models.ImageField(default='default.png', upload_to='thumbnails')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1000)),
                ('edited', models.CharField(default='0', max_length=1)),
                ('datePosted', models.DateField(auto_now_add=True)),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
        ),
    ]
