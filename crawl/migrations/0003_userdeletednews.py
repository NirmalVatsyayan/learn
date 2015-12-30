# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crawl', '0002_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDeletedNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('news', models.ManyToManyField(related_name='news_deleted', to='crawl.News')),
                ('user', models.ForeignKey(related_name='delete_news_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
