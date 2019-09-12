# Generated by Django 2.2.5 on 2019-09-11 10:28

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0006_auto_20190910_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionlevel',
            name='session_data',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='crops',
            name='crop_type',
            field=models.CharField(choices=[('FRUITS', 'FRUITS'), ('VEGETABLES', 'VEGETABLES')], default='FRUITS', max_length=20),
        ),
    ]
