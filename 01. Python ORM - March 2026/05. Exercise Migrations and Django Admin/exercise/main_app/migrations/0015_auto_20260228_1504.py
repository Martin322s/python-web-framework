from datetime import timedelta
from django.db import migrations


def update_orders(apps, schema_editor):
    Order = apps.get_model("main_app", "Order")

    # 1) Cancelled -> delete
    Order.objects.filter(status="Cancelled").delete()

    # 2) Pending -> delivery = order_date + 3 days
    for o in Order.objects.filter(status="Pending"):
        o.delivery = o.order_date + timedelta(days=3)
        o.save(update_fields=["delivery"])

    # 3) Completed -> warranty = "24 months"
    Order.objects.filter(status="Completed").update(warranty="24 months")


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0014_order"),
    ]

    operations = [
        migrations.RunPython(update_orders, migrations.RunPython.noop),
    ]