# Generated by Django 3.2.13 on 2022-05-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ty', '0015_alter_book_maximum_no_of_borrowing_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='no_of_book_available',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='maximum_no_of_borrowing_days',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='borrower_record',
            name='borrower_user_details',
            field=models.ManyToManyField(blank=True, to='ty.Borrower_User'),
        ),
        migrations.AlterField(
            model_name='borrower_user',
            name='user_details',
            field=models.ManyToManyField(blank=True, to='ty.Book_Return_And_History'),
        ),
    ]
