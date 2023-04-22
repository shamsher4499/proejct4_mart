# Generated by Django 4.1.7 on 2023-03-20 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='humanchatdata',
            name='reciever',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever_user', to=settings.AUTH_USER_MODEL),
        ),
    ]