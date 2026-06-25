from django.db import migrations

AIRPODS_MODELS = [
    {
        "name": "AirPods Pro 1",
        "slug": "airpods-pro-1",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-pro-1-earbuds.png",
        "sort_order": 10,
    },
    {
        "name": "AirPods Pro 2",
        "slug": "airpods-pro-2",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-pro-2-earbuds.png",
        "sort_order": 20,
    },
    {
        "name": "AirPods Pro 3",
        "slug": "airpods-pro-3",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-pro-3-earbuds.png",
        "sort_order": 30,
    },
    {
        "name": "AirPods 1",
        "slug": "airpods-1",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-1-earbuds.png",
        "sort_order": 40,
    },
    {
        "name": "AirPods 2",
        "slug": "airpods-2",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-2-earbuds.png",
        "sort_order": 50,
    },
    {
        "name": "AirPods 3",
        "slug": "airpods-3",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-3-earbuds.png",
        "sort_order": 60,
    },
    {
        "name": "AirPods 4",
        "slug": "airpods-4",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-4-earbuds.png",
        "sort_order": 70,
    },
    {
        "name": "AirPods 4 ANC",
        "slug": "airpods-4-anc",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-4-anc-earbuds.png",
        "sort_order": 80,
    },
    {
        "name": "I am not sure",
        "slug": "unknown-earbuds",
        "kind": "earbuds",
        "image_path": "assets/airpods/products/web/airpods-pro-2-earbuds.png",
        "sort_order": 999,
    },
    {
        "name": "A1602 - AirPods 1/2 Lightning case",
        "slug": "a1602-airpods-1-2-lightning-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A1602.png",
        "sort_order": 10,
    },
    {
        "name": "A1938 - AirPods 1/2 Wireless case",
        "slug": "a1938-airpods-1-2-wireless-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A1938.png",
        "sort_order": 20,
    },
    {
        "name": "A2566 - AirPods 3 MagSafe case",
        "slug": "a2566-airpods-3-magsafe-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2566-magsafe.png",
        "sort_order": 30,
    },
    {
        "name": "A2897 - AirPods 3 Lightning case",
        "slug": "a2897-airpods-3-lightning-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2897-lightning.png",
        "sort_order": 40,
    },
    {
        "name": "A3058 - AirPods 4 case",
        "slug": "a3058-airpods-4-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A3058.png",
        "sort_order": 50,
    },
    {
        "name": "A3059 - AirPods 4 ANC case",
        "slug": "a3059-airpods-4-anc-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A3059-ANC.png",
        "sort_order": 60,
    },
    {
        "name": "A2190 - AirPods Pro 1 case",
        "slug": "a2190-airpods-pro-1-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2190.png",
        "sort_order": 70,
    },
    {
        "name": "A2700 - AirPods Pro 2 Lightning case",
        "slug": "a2700-airpods-pro-2-lightning-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2700-magsafe-lightning.png",
        "sort_order": 80,
    },
    {
        "name": "A2968 - AirPods Pro 2 USB-C case",
        "slug": "a2968-airpods-pro-2-usb-c-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2968-magsafe-lightning.png",
        "sort_order": 90,
    },
    {
        "name": "A3122 - AirPods Pro 3 USB-C case",
        "slug": "a3122-airpods-pro-3-usb-c-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A3122-magsafe.png",
        "sort_order": 100,
    },
    {
        "name": "I am not sure",
        "slug": "unknown-case",
        "kind": "case",
        "image_path": "assets/airpods/cases/web/A2968-magsafe-lightning.png",
        "sort_order": 999,
    },
]


def seed_airpods_models(apps, schema_editor):
    airpods_model = apps.get_model("pages", "AirPodsModel")
    for model in AIRPODS_MODELS:
        airpods_model.objects.update_or_create(slug=model["slug"], defaults=model)


def remove_seeded_airpods_models(apps, schema_editor):
    airpods_model = apps.get_model("pages", "AirPodsModel")
    airpods_model.objects.filter(slug__in=[model["slug"] for model in AIRPODS_MODELS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_airpods_models, remove_seeded_airpods_models),
    ]
