# Generated by Django 4.2.15 on 2024-09-24 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_alter_session_attendance_session_attended_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prayer_cell_feedback',
            name='disciple_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]