# Generated by Django 3.2.13 on 2022-05-05 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ty', '0007_auto_20220505_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]