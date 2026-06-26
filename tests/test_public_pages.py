import pytest
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile

from pages.forms import MAX_PHOTO_SIZE_BYTES, PHOTO_SLOTS
from pages.models import (
    AirPodsModel,
    SellerSubmission,
    SellerSubmissionItem,
    SellerSubmissionItemPhoto,
)


@pytest.mark.parametrize("path", ["/", "/sell/", "/impressum.html", "/datenschutz.html"])
@pytest.mark.django_db
def test_public_pages_return_200(client, path):
    response = client.get(path)

    assert response.status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "/static/style.css",
        "/static/logo.png",
        "/static/assets/favicons/favicon-32x32.png",
        "/static/assets/logo/logo-master.svg",
        "/static/assets/hero/airpods-reunion-hero.mp4",
        "/static/assets/airpods/products/web/airpods-pro-2-with-case-front.png",
    ],
)
def test_representative_static_assets_return_200(client, path):
    response = client.get(path)

    assert response.status_code == 200


def photo_upload(name="photo.jpg", content=b"photo"):
    return SimpleUploadedFile(name, content, content_type="image/jpeg")


def add_required_photos(data, part_type):
    for slot, _label in PHOTO_SLOTS[part_type]:
        data[f"photo_{part_type}_{slot}"] = photo_upload(f"{part_type}_{slot}.jpg")


def valid_submission_data():
    earbud_model = AirPodsModel.objects.filter(
        kind=AirPodsModel.Kind.EARBUDS, is_active=True
    ).first()
    case_model = AirPodsModel.objects.filter(kind=AirPodsModel.Kind.CASE, is_active=True).first()
    data = {
        "parts": [SellerSubmissionItem.PartType.LEFT, SellerSubmissionItem.PartType.CASE],
        "seller_name": "Alex Seller",
        "contact_email": "alex@example.com",
        "street_address": "Example Street 12",
        "postal_code": "10115",
        "city": "Berlin",
        "country": "Germany",
        "shipping_possible": "on",
        "local_handoff_possible": "on",
        "notes": "Happy to ship quickly.",
        "item_left_airpods_model": str(earbud_model.pk),
        "item_left_model_number": "A2699",
        "item_left_condition": SellerSubmissionItem.Condition.GOOD,
        "item_left_asking_price_eur": "49.00",
        "item_left_cleaned_and_ready": "on",
        "item_case_airpods_model": str(case_model.pk),
        "item_case_model_number": "A2968",
        "item_case_condition": SellerSubmissionItem.Condition.EXCELLENT,
        "item_case_asking_price_eur": "59.00",
        "item_case_cleaned_and_ready": "on",
    }
    add_required_photos(data, SellerSubmissionItem.PartType.LEFT)
    add_required_photos(data, SellerSubmissionItem.PartType.CASE)
    return data


@pytest.mark.django_db
def test_valid_multi_item_seller_submission_saves_parent_items_and_photos(
    client, settings, tmp_path
):
    settings.MEDIA_ROOT = tmp_path

    response = client.post("/sell/", valid_submission_data())

    assert response.status_code == 302
    submission = SellerSubmission.objects.get()
    assert submission.seller_name == "Alex Seller"
    assert submission.full_address == "Example Street 12, 10115, Berlin, Germany"
    assert submission.items.count() == 2
    assert SellerSubmissionItemPhoto.objects.count() == (
        len(PHOTO_SLOTS[SellerSubmissionItem.PartType.LEFT])
        + len(PHOTO_SLOTS[SellerSubmissionItem.PartType.CASE])
    )


@pytest.mark.django_db
def test_duplicate_part_types_in_one_submission_are_rejected(client):
    data = {"parts": [SellerSubmissionItem.PartType.LEFT, SellerSubmissionItem.PartType.LEFT]}

    response = client.post("/sell/", data)

    assert response.status_code == 200
    assert SellerSubmission.objects.count() == 0
    assert b"Select each part type only once" in response.content


@pytest.mark.django_db
def test_missing_required_photo_slot_is_rejected(client):
    data = valid_submission_data()
    data.pop("photo_left_stem")

    response = client.post("/sell/", data)

    assert response.status_code == 200
    assert SellerSubmission.objects.count() == 0
    assert b"Stem photo is required" in response.content


@pytest.mark.django_db
def test_invalid_photo_extension_is_rejected(client):
    data = valid_submission_data()
    data["photo_left_stem"] = photo_upload("stem.gif")

    response = client.post("/sell/", data)

    assert response.status_code == 200
    assert SellerSubmission.objects.count() == 0
    assert b"Upload a JPG, PNG, WebP, HEIC, or HEIF photo" in response.content


@pytest.mark.django_db
def test_too_large_photo_is_rejected(client):
    data = valid_submission_data()
    data["photo_left_stem"] = photo_upload("stem.jpg", b"x" * (MAX_PHOTO_SIZE_BYTES + 1))

    response = client.post("/sell/", data)

    assert response.status_code == 200
    assert SellerSubmission.objects.count() == 0
    assert b"Please upload a photo under 20 MB" in response.content


@pytest.mark.django_db
def test_honeypot_submission_is_not_saved(client):
    response = client.post("/sell/", {"company_website": "https://spam.example"})

    assert response.status_code == 302
    assert SellerSubmission.objects.count() == 0


def test_seller_submission_models_are_registered_in_admin():
    assert AirPodsModel in admin.site._registry
    assert SellerSubmission in admin.site._registry
    assert SellerSubmissionItem in admin.site._registry
    assert SellerSubmissionItemPhoto in admin.site._registry


@pytest.mark.django_db
def test_model_dropdowns_only_include_active_compatible_models(client):
    inactive = AirPodsModel.objects.create(
        name="Inactive AirPods",
        slug="inactive-airpods",
        kind=AirPodsModel.Kind.EARBUDS,
        is_active=False,
    )

    response = client.get("/sell/")

    assert response.status_code == 200
    assert inactive not in response.context["parts"][0]["models"]
    for part in response.context["parts"]:
        expected_kind = (
            AirPodsModel.Kind.CASE
            if part["value"] == SellerSubmissionItem.PartType.CASE
            else AirPodsModel.Kind.EARBUDS
        )
        assert all(model.is_active and model.kind == expected_kind for model in part["models"])
