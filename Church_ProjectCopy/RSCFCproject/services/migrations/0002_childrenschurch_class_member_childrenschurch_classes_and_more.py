# Generated by Django 4.2.15 on 2024-10-21 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='childrensChurch_class_member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.people')),
            ],
        ),
        migrations.CreateModel(
            name='childrensChurch_classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=30)),
                ('head_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='childrensChurch_teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ManyToManyField(to='services.childrenschurch_classes')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='class_service_feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_taught', models.TextField(verbose_name='Word Taught:')),
                ('general_feedback', models.TextField(verbose_name='General Feedback:')),
                ('requires_attention', models.TextField(verbose_name='Requires Attention:')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.childrenschurch_classes')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(to='services.childrenschurch_teachers')),
            ],
        ),
        migrations.CreateModel(
            name='class_attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateofclass', models.DateField(default=django.utils.timezone.now, verbose_name='Date:')),
                ('service', models.CharField(choices=[('1', 'First Servce'), ('2', 'Second Service')], max_length=3)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.childrenschurch_class_member')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.childrenschurch_classes')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='childrenschurch_class_member',
            name='class_attending',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.childrenschurch_classes'),
        ),
    ]