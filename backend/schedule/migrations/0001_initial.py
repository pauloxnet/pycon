# Generated by Django 2.1.7 on 2019-05-11 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('type', models.CharField(choices=[('submission', 'Submission'), ('custom', 'Custom')], max_length=10, verbose_name='type')),
                ('additional_speakers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='additional speakers')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_items', to='conferences.Conference', verbose_name='conference')),
                ('rooms', models.ManyToManyField(related_name='talks', to='schedule.Room', verbose_name='rooms')),
            ],
            options={
                'verbose_name': 'Schedule item',
                'verbose_name_plural': 'Schedule items',
            },
        ),
    ]
