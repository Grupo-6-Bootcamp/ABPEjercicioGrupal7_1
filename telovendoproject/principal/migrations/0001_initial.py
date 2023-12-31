# Generated by Django 4.2.2 on 2023-07-06 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('rut', models.CharField(max_length=12)),
                ('direccion', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=50)),
                ('idusuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('valor_unit', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=100)),
                ('imagen', models.ImageField(default='producto_default.png', upload_to='media/images')),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductoWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_deseada', models.PositiveIntegerField()),
                ('idproducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('idcliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.cliente')),
                ('productos', models.ManyToManyField(through='principal.ProductoWishlist', to='principal.producto')),
            ],
        ),
        migrations.AddField(
            model_name='productowishlist',
            name='idwishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='principal.wishlist'),
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('direccion_despacho', models.CharField(max_length=100)),
                ('fecha_despacho', models.DateTimeField()),
                ('subtotal', models.PositiveIntegerField()),
                ('valordespacho', models.PositiveIntegerField()),
                ('valortotal', models.PositiveIntegerField()),
                ('metododepago', models.CharField(choices=[('Transferencia', 'Transferencia'), ('Tarjeta de Credito', 'Tarjeta de Crédito'), ('Tarjeta de Debito', 'Tarjeta de Débito')], max_length=50)),
                ('estadopedido', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En preparacion', 'En preparación'), ('Entregado', 'Entregado'), ('En Despacho', 'En Despacho')], max_length=50)),
                ('wishlist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='principal.wishlist')),
            ],
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('valor_unit', models.PositiveIntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='principal.pedido')),
                ('productos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='principal.producto')),
            ],
        ),
    ]
