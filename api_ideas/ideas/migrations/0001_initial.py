# Generated by Django 3.0.7 on 2020-06-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.CharField(max_length=254)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'The idea is public and available by someone'), (2, 'The idea is protected and available by followers'), (3, 'The idea is privated and not available')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
