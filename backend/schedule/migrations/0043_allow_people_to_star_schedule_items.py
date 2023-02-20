# Generated by Django 4.1.6 on 2023-02-16 13:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0042_add_panel_as_schedule_item_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItemStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('user_id', models.IntegerField(db_index=True, verbose_name='user')),
                ('schedule_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='schedule.scheduleitem', verbose_name='schedule item')),
            ],
            options={
                'unique_together': {('user_id', 'schedule_item')},
            },
        ),
    ]
