from django.db import migrations


def set_category_by_price(apps, schema_editor):
    Smartphone = apps.get_model("main_app", "Smartphone")

    for s in Smartphone.objects.all():
        s.category = "Expensive" if s.price >= 750 else "Cheap"
        s.save(update_fields=["category"])


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0012_auto_20260228_1502"),
    ]

    operations = [
        migrations.RunPython(set_category_by_price, migrations.RunPython.noop),
    ]