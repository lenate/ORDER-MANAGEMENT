# Generated by Django 4.0.5 on 2022-06-02 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce1', '0005_user_if_logged_user_password_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
