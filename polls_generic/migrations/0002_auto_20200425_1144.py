# Generated by Django 3.0.5 on 2020-04-25 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls_generic', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
