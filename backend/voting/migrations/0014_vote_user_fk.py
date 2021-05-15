# Generated by Django 3.1.4 on 2021-05-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0013_submission_comment_author_fk'),
        ('voting', '0013_auto_20200202_1830'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterField(
                    model_name='vote',
                    name='user',
                    field=models.ForeignKey('users.User', db_constraint=False, db_index=True, null=False, on_delete=models.PROTECT, related_name="votes")
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name='vote',
                    name='user',
                ),
                migrations.AddField(
                    model_name='vote',
                    name='user_id',
                    field=models.IntegerField(verbose_name='user'),
                ),
                migrations.AlterUniqueTogether(
                    name='vote',
                    unique_together={('user_id', 'submission')},
                ),
            ]
        ),
    ]
