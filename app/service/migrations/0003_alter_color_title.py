# Generated by Django 5.0.4 on 2024-04-14 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_color_palette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='title',
            field=models.CharField(blank=True, help_text='Оставьте пустым и название будет сгенерировано автоматически', max_length=50, verbose_name='Название'),
        ),
    ]
