# Generated by Django 2.2.7 on 2019-12-23 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotsearchwords',
            options={'ordering': ['id'], 'verbose_name': '热搜排行', 'verbose_name_plural': '热搜排行'},
        ),
    ]