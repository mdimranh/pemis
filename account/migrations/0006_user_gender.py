# Generated by Django 4.2.4 on 2023-10-12 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_verify_email_code_expired_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ("Other's", 'others')], default='male', max_length=10),
        ),
    ]
