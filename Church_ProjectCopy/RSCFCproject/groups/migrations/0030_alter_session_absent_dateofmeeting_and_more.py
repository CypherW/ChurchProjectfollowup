# Generated by Django 4.2.15 on 2024-09-07 19:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0029_alter_session_absent_dateofmeeting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_absent',
            name='dateofmeeting',
            field=models.DateField(default=datetime.date(2024, 9, 7), verbose_name='Date:'),
        ),
        migrations.AlterField(
            model_name='session_absent',
            name='follow_up_date',
            field=models.DateField(default=datetime.date(2024, 9, 7), verbose_name='Date:'),
        ),
        migrations.AlterField(
            model_name='session_attendance',
            name='dateofvisit',
            field=models.DateField(default=datetime.date(2024, 9, 7), verbose_name='Date:'),
        ),
    ]