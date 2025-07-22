from django.db import migrations

def migrate_account_data(apps, schema_editor):
    """
    Migra los datos de GenericForeignKey a ForeignKey
    """
    AccountMovement = apps.get_model('banco', 'AccountMovement')
    DebtorAccount = apps.get_model('banco', 'DebtorAccount')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Obtener el ContentType para DebtorAccount
    debtor_account_ct = ContentType.objects.get_for_model(DebtorAccount)
    
    # Actualizar todos los movimientos que apuntan a DebtorAccount
    AccountMovement.objects.filter(
        content_type=debtor_account_ct
    ).update(
        account_id=models.F('object_id')
    )

class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0002_accountmovement_account_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_account_data),
    ] 