# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article2tag',
            options={'verbose_name': '标签名称和文章关系表', 'verbose_name_plural': '标签名称和文章关系表'},
        ),
        migrations.AlterModelOptions(
            name='articleupdown',
            options={'verbose_name': '文章点赞表', 'verbose_name_plural': '文章点赞表'},
        ),
        migrations.AlterModelOptions(
            name='commentup',
            options={'verbose_name': '评论点赞表', 'verbose_name_plural': '评论点赞表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签名称表', 'verbose_name_plural': '标签名称表'},
        ),
        migrations.AddField(
            model_name='comment',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='被踩次数'),
        ),
        migrations.AddField(
            model_name='commentup',
            name='UpOrDown',
            field=models.BooleanField(default=False, verbose_name='是否赞'),
        ),
        migrations.AlterField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(default=0, verbose_name='评论次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(default=0, verbose_name='被踩次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='read_count',
            field=models.IntegerField(default=0, verbose_name='阅读次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞次数'),
        ),
        migrations.AlterField(
            model_name='articledetail',
            name='nid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='up_count',
            field=models.IntegerField(default=0, verbose_name='点赞次数'),
        ),
    ]