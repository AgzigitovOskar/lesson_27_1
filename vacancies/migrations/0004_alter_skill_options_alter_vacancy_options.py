# Generated by Django 4.1.5 on 2023-01-23 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_skill_vacancy_skills'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'Навык', 'verbose_name_plural': 'Навыки'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]