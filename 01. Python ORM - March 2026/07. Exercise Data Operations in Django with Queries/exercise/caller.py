import os
from decimal import Decimal
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from django.db import models
# Create queries within functions

def create_pet(name, species):
    pet = Pet.objects.create(name=name, species=species)
    return f"{pet.name} is a very cute {pet.species}!"

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact.objects.create(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact, new_name):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()

def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    result = []

    for location in locations:
        result.append(f"{location.name} has a population of {location.population}!")

    return '\n'.join(result)

def new_capital():
    capital = Location.objects.first()
    capital.is_capital = True
    capital.save()

def get_capitals():
    return Location.objects.filter(is_capital=True)

def delete_first_location():
    Location.objects.first().delete()

def apply_discount():
    for car in Car.objects.all():
        discount_percent = sum(int(d) for d in str(car.year))  # e.g. 2014 -> 7
        multiplier = Decimal("1") - (Decimal(discount_percent) / Decimal("100"))
        car.price_with_discount = (car.price * multiplier).quantize(Decimal("0.01"))
        car.save(update_fields=["price_with_discount"])

def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values("model", "price_with_discount")

def delete_last_car():
    last_car = Car.objects.last()
    if last_car is not None:
        last_car.delete()

def show_unfinished_tasks():
    qs = Task.objects.filter(is_finished=False).values_list("title", "due_date")
    return "\n".join([f"Task - {title} needs to be done until {due_date}!" for title, due_date in qs])

def complete_odd_tasks():
    Task.objects.filter(id__mod=(2, 1)).update(is_finished=True)

def encode_and_replace(text: str, task_title: str):
    decoded = "".join(chr(ord(ch) - 3) for ch in text)
    Task.objects.filter(title=task_title).update(description=decoded)

def get_deluxe_rooms():
    qs = (
        HotelRoom.objects.filter(room_type="Deluxe", id__mod=(2, 0))
        .values_list("room_number", "price_per_night")
        .order_by("id")
    )
    return "\n".join(
        [f"Deluxe room with number {room_number} costs {price_per_night}$ per night!" for room_number, price_per_night in qs]
    )

def increase_room_capacity():
    rooms = list(HotelRoom.objects.order_by("id"))

    for idx, room in enumerate(rooms):
        if not room.is_reserved:
            continue

        if idx == 0:
            room.capacity += room.id
        else:
            room.capacity += rooms[idx - 1].capacity

        room.save(update_fields=["capacity"])


def reserve_first_room():
    first_room = HotelRoom.objects.order_by("id").first()
    if first_room is not None:
        first_room.is_reserved = True
        first_room.save(update_fields=["is_reserved"])

def delete_last_room():
    last_room = HotelRoom.objects.order_by("id").last()
    if last_room is not None and not last_room.is_reserved:
        last_room.delete()

def update_characters():
    Character.objects.filter(class_name="Mage").update(
        level=models.F("level") + 3,
        intelligence=models.F("intelligence") - 7,
    )

    # "decrease hit points by half" -> interpret as integer half
    for ch in Character.objects.filter(class_name="Warrior"):
        ch.hit_points = ch.hit_points // 2
        ch.dexterity += 4
        ch.save(update_fields=["hit_points", "dexterity"])

    Character.objects.filter(class_name__in=["Assassin", "Scout"]).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character: Character, second_character: Character):
    name = f"{first_character.name} {second_character.name}"
    level = (first_character.level + second_character.level) // 2

    strength = int((first_character.strength + second_character.strength) * 1.2)
    dexterity = int((first_character.dexterity + second_character.dexterity) * 1.4)
    intelligence = int((first_character.intelligence + second_character.intelligence) * 1.5)

    hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        inventory = "Dragon Scale Armor, Excalibur"

    # delete materials
    first_character.delete()
    second_character.delete()

    # create fusion
    fusion = Character.objects.create(
        name=name,
        class_name="Fusion",
        level=level,
        strength=strength,
        dexterity=dexterity,
        intelligence=intelligence,
        hit_points=hit_points,
        inventory=inventory,
    )
    return fusion

def grand_dexterity():
    Character.objects.update(dexterity=30)

def grand_intelligence():
    Character.objects.update(intelligence=40)

def grand_strength():
    Character.objects.update(strength=50)

def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()

