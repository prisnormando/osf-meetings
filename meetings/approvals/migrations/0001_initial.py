# -*- coding: utf-8 -*-
<<<<<<< e2d45ac04fd1caa30e18215eb0544a8d026efee5
# Generated by Django 1.9.7 on 2016-07-20 20:06

=======
# Generated by Django 1.9.8 on 2016-08-01 18:14
>>>>>>> migrations
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('view_approval', 'Can view approval'),),
            },
        ),
    ]
