# Generated by Django 2.2.5 on 2019-09-07 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussd', '0002_auto_20190907_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fruits',
            options={'verbose_name_plural': 'Fruits'},
        ),
        migrations.AlterModelOptions(
            name='sagurausers',
            options={'verbose_name_plural': 'Sagura Users'},
        ),
        migrations.AlterModelOptions(
            name='subscribers',
            options={'verbose_name_plural': ' Subscribers'},
        ),
        migrations.AlterModelOptions(
            name='vegetables',
            options={'verbose_name_plural': ' Vegetables'},
        ),
        migrations.AlterField(
            model_name='sessionlevel',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
