# Generated by Django 4.2.4 on 2023-08-10 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabdeal_B2B', '0007_rename_increasecredits_increasecredit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='credits',
            new_name='credit',
        ),
    ]
