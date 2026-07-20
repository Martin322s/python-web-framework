from django.db import migrations

def set_item_rarity(apps, schema_editor):
    Item = apps.get_model("main_app", "Item")

    for it in Item.objects.all():
        price = it.price  # Decimal
        if price <= 10:
            it.rarity = "Rare"
        elif 11 <= price <= 20:
            it.rarity = "Very Rare"
        elif 21 <= price <= 30:
            it.rarity = "Extremely Rare"
        else:
            it.rarity = "Mega Rare"
        it.save(update_fields=["rarity"])


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0009_item"),
    ]

    operations = [
        migrations.RunPython(set_item_rarity, migrations.RunPython.noop),
    ]