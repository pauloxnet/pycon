# Generated by Django 2.2.8 on 2020-01-16 13:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0010_submissioncomment'),
        ('conferences', '0017_auto_20191231_1607'),
        ('voting', '0007_auto_20200116_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conferences.Conference', verbose_name='conference')),
            ],
        ),
        migrations.CreateModel(
            name='RankSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absolute_rank', models.PositiveIntegerField(verbose_name='absolute rank')),
                ('absolute_score', models.PositiveIntegerField(verbose_name='absolute score')),
                ('topic_rank', models.PositiveIntegerField(verbose_name='topic rank')),
                ('topic_score', models.PositiveIntegerField(verbose_name='topic score')),
                ('rank_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank_submissions', to='voting.RankRequest', verbose_name='rank request')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.Submission', verbose_name='submission')),
            ],
        ),
    ]