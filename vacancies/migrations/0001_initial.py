# Generated by Django 4.1.5 on 2023-01-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('text', models.CharField(max_length=2000)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('open', 'Открыта'), ('closed', 'Закрыта')], default='draft', max_length=6)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
