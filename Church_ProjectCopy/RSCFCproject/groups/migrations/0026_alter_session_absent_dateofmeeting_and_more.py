# Generated by Django 5.0.7 on 2024-07-28 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0025_alter_session_attendance_dateofvisit_session_absent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_absent',
            name='dateofmeeting',
            field=models.DateField(default=datetime.date(2024, 7, 28), verbose_name='Date:'),
        ),
        migrations.AlterField(
            model_name='session_attendance',
            name='dateofvisit',
            field=models.DateField(default=datetime.date(2024, 7, 28), verbose_name='Date:'),
        ),
    ]