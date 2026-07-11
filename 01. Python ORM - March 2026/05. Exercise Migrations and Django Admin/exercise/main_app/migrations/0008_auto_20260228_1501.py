from django.db import migrations

def set_age_groups(apps, schema_editor):
    Person = apps.get_model("main_app", "Person")

    for p in Person.objects.all():
        if p.age <= 12:
            p.age_group = "Child"
        elif 13 <= p.age <= 17:
            p.age_group = "Teen"
        else:
            p.age_group = "Adult"
        p.save(update_fields=["age_group"])


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0007_person"),
    ]

    operations = [
        migrations.RunPython(set_age_groups, migrations.RunPython.noop),
    ]