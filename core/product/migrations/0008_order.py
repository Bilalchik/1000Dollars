# Generated by Django 4.2.20 on 2025-04-19 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0007_basket_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.PositiveBigIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('address', models.CharField(max_length=225)),
                ('status', models.CharField(choices=[('in_progress', 'В обработке'), ('accepted', 'Принято'), ('denied', 'Отклонено')], default='in_progress', max_length=13)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('baskets', models.ManyToManyField(to='product.basket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
