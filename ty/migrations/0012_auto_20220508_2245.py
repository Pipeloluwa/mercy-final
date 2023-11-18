# Generated by Django 3.2.13 on 2022-05-08 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ty', '0011_book_return_and_history_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrower_user',
            name='user_details',
        ),
        migrations.AddField(
            model_name='borrower_user',
            name='user_details',
            field=models.ManyToManyField(blank=True, null=True, to='ty.Book_Return_And_History'),
        ),
    ]
