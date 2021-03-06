# Generated by Django 2.2.3 on 2019-07-24 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Traceback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('is_request', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trace_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Traceback')),
            ],
            options={
                'verbose_name': 'Traceback',
                'verbose_name_plural': 'Tracebacks',
            },
        ),
    ]
