# Generated by Django 2.2.2 on 2019-07-05 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribe',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, verbose_name='邮箱'),
        ),
    ]
