# Generated by Django 4.2.15 on 2024-09-30 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_alter_prayer_cell_feedback_disciple_leader'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SalvationFollowUps', '0002_new_convert_followup_call_new_convert_first_followup'),
    ]

    operations = [
        migrations.CreateModel(
            name='new_convert_referral_finalize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer_to_church', models.TextField(verbose_name='Refer to another church:')),
                ('finalize', models.BooleanField()),
                ('date_of_followup', models.DateField(default=django.utils.timezone.now, verbose_name='Date:')),
                ('convert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalvationFollowUps.salvations')),
                ('followedup_up_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('refer_to_prayer_cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.session_attended_options')),
            ],
            options={
                'verbose_name_plural': 'New Convert Referral and Finalize',
            },
        ),
    ]