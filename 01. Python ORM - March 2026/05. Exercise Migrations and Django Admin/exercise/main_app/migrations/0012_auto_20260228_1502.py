from decimal import Decimal
from django.db import migrations


def set_price_by_brand_length(apps, schema_editor):
    Smartphone = apps.get_model("main_app", "Smartphone")

    for s in Smartphone.objects.all():
        s.price = Decimal(len(s.brand) * 120)
        s.save(update_fields=["price"])


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0011_smartphone"),
    ]

    operations = [
        migrations.RunPython(set_price_by_brand_length, migrations.RunPython.noop),
    ]