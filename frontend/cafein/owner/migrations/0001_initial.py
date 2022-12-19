# Generated by Django 3.2 on 2022-12-09 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.EmailField(default='', max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(default='', max_length=300)),
                ('phone', models.CharField(default='', max_length=25, unique=True)),
                ('cafe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cafe.cafe')),
            ],
            
            options={
                'db_table': 'owner',
            },
        ),
        migrations.AddField(
            model_name='owner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='owner',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='owner',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='email',
            field=models.EmailField(default='', max_length=100, unique=True, verbose_name='email'),
        ),
    ]
