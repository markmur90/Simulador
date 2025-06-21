from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0006_add_movimientos'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('DEPOSIT', 'Depósito'), ('PAYMENT', 'Pago')], max_length=10)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos', to='banco.debtoraccount')),
            ],
        ),
    ]