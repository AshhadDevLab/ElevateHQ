# Generated by Django 5.1.1 on 2024-09-20 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_subscription_subtitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['order', 'featured', '-updated'], 'permissions': [('advanced', 'Advanced Permission'), ('pro', 'Pro Permission'), ('basic', 'Basic Permission'), ('enterprise', 'Enterprise Permission')]},
        ),
    ]
