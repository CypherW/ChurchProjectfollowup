# Generated by Django 4.2.15 on 2024-09-10 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalvationFollowUps', '0032_alter_followups_next_followupdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followups',
            name='next_followUpdate',
            field=models.DateTimeField(default=datetime.date(2024, 9, 10)),
        ),
        migrations.AlterField(
            model_name='salvations',
            name='dateofcommitment',
            field=models.DateField(default=datetime.date(2024, 9, 10), verbose_name='Date:'),
        ),
    ]