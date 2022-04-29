# Generated by Django 3.2.12 on 2022-03-31 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0026_move_speaker_voucher_in_conferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speakervoucher',
            name='pretix_voucher_id',
            field=models.IntegerField(blank=True, help_text='ID of the voucher in the Pretix database', null=True),
        ),
    ]