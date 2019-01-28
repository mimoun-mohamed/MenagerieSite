# Generated by Django 2.1.5 on 2019-01-18 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('state', models.CharField(choices=[('HU', 'affame'), ('TI', 'fatigue'), ('SA', 'repus'), ('SL', 'endormi')], default='SA', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('availability', models.BooleanField()),
                ('user_limit', models.IntegerField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lamenageriemanager.Equipment'),
        ),
    ]
