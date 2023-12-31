# Generated by Django 4.2.7 on 2023-11-29 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silmarin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название квеста')),
                ('description', models.TextField(verbose_name='Описание')),
                ('quantity', models.IntegerField(help_text='Введите необходимое количество участников', max_length=200, verbose_name='Количество')),
                ('statuses', models.ManyToManyField(to='silmarin.status')),
            ],
            options={
                'db_table': 'Quests',
            },
        ),
    ]
