# Generated by Django 5.1.7 on 2025-03-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stock', models.IntegerField()),
                ('category', models.CharField(choices=[('FR', 'Fruits'), ('VE', 'Vegetables'), ('MT', 'Meats'), ('DA', 'Dairy'), ('HY', 'Hygiene'), ('CL', 'Cleaning'), ('FZ', 'Frozen'), ('SF', 'Sea Food'), ('PR', 'Preserves'), ('BG', 'Baked Goods')], max_length=2)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
