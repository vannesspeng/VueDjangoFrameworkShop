# Generated by Django 2.0.2 on 2018-11-06 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_hotsearchwords_indexad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='goods_font_image',
            new_name='goods_front_image',
        ),
    ]
