# Generated by Django 4.2.6 on 2023-12-04 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_room_participants_alter_room_roomid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='chat.room'),
        ),
    ]