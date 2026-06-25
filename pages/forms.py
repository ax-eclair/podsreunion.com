from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from .models import AirPodsModel, SellerSubmission, SellerSubmissionItem, SellerSubmissionItemPhoto

MAX_PHOTO_SIZE_BYTES = 20 * 1024 * 1024
ALLOWED_PHOTO_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "heic", "heif"}

PHOTO_SLOTS = {
    SellerSubmissionItem.PartType.LEFT: [
        ("exterior_side", "Exterior side"),
        ("interior_grille", "Interior grille"),
        ("stem", "Stem"),
        ("model_number", "Model number"),
    ],
    SellerSubmissionItem.PartType.RIGHT: [
        ("exterior_side", "Exterior side"),
        ("interior_grille", "Interior grille"),
        ("stem", "Stem"),
        ("model_number", "Model number"),
    ],
    SellerSubmissionItem.PartType.CASE: [
        ("front_closed", "Front closed"),
        ("back_hinge", "Back hinge"),
        ("inside_open", "Inside open"),
        ("charging_port", "Charging port"),
        ("model_number", "Model number"),
        ("led_on", "LED on"),
    ],
}

PART_TYPE_LABELS = dict(SellerSubmissionItem.PartType.choices)
CONDITION_LABELS = dict(SellerSubmissionItem.Condition.choices)
PHOTO_FIELD_PREFIX = "photo"


def required_slots_for_part(part_type):
    return PHOTO_SLOTS[part_type]


def model_kind_for_part(part_type):
    if part_type == SellerSubmissionItem.PartType.CASE:
        return AirPodsModel.Kind.CASE
    return AirPodsModel.Kind.EARBUDS


def validate_uploaded_photo(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower().lstrip(".")
    if extension not in ALLOWED_PHOTO_EXTENSIONS:
        raise ValidationError("Upload a JPG, PNG, WebP, HEIC, or HEIF photo.")

    if uploaded_file.size > MAX_PHOTO_SIZE_BYTES:
        raise ValidationError("Please upload a photo under 20 MB.")


def _required_text(post_data, field_name, errors, label):
    value = post_data.get(field_name, "").strip()
    if not value:
        errors[field_name] = f"{label} is required."
    return value


def _parse_price(raw_price, field_name, errors):
    try:
        price = Decimal(raw_price)
    except (InvalidOperation, TypeError):
        errors[field_name] = "Enter a valid price in EUR."
        return None

    if price <= 0:
        errors[field_name] = "Enter a price greater than 0."
        return None

    return price


def validate_seller_submission_request(post_data, files):
    errors = {}
    selected_parts = post_data.getlist("parts")
    valid_parts = set(PHOTO_SLOTS)

    if not selected_parts:
        errors["parts"] = "Select at least one part."

    if len(selected_parts) != len(set(selected_parts)):
        errors["parts"] = "Select each part type only once."

    invalid_parts = [part for part in selected_parts if part not in valid_parts]
    if invalid_parts:
        errors["parts"] = "Select a valid part type."

    payload = {
        "submission": {
            "seller_name": _required_text(post_data, "seller_name", errors, "Seller name"),
            "contact_email": _required_text(post_data, "contact_email", errors, "Contact email"),
            "street_address": _required_text(post_data, "street_address", errors, "Street address"),
            "postal_code": _required_text(post_data, "postal_code", errors, "Postal code"),
            "city": _required_text(post_data, "city", errors, "City"),
            "country": _required_text(post_data, "country", errors, "Country"),
            "shipping_possible": post_data.get("shipping_possible") == "on",
            "local_handoff_possible": post_data.get("local_handoff_possible") == "on",
            "notes": post_data.get("notes", "").strip(),
        },
        "items": [],
    }

    if payload["submission"]["contact_email"]:
        try:
            validate_email(payload["submission"]["contact_email"])
        except ValidationError:
            errors["contact_email"] = "Enter a valid contact email."

    for part_type in selected_parts:
        if part_type not in valid_parts:
            continue

        prefix = f"item_{part_type}"
        model_field = f"{prefix}_airpods_model"
        model_id = post_data.get(model_field)
        model = None
        try:
            model = AirPodsModel.objects.get(
                pk=model_id,
                kind=model_kind_for_part(part_type),
                is_active=True,
            )
        except (AirPodsModel.DoesNotExist, ValueError, TypeError):
            errors[model_field] = "Select an active compatible model."

        condition_field = f"{prefix}_condition"
        condition = post_data.get(condition_field, "")
        if condition not in SellerSubmissionItem.Condition.values:
            errors[condition_field] = "Select a valid condition."

        price_field = f"{prefix}_asking_price_eur"
        price = _parse_price(post_data.get(price_field), price_field, errors)

        cleaned_field = f"{prefix}_cleaned_and_ready"
        cleaned_and_ready = post_data.get(cleaned_field) == "on"
        if not cleaned_and_ready:
            errors[cleaned_field] = "Confirm this item has been cleaned and is ready to ship."

        model_number = _required_text(post_data, f"{prefix}_model_number", errors, "Model number")

        photos = []
        for slot, label in required_slots_for_part(part_type):
            file_field = f"{PHOTO_FIELD_PREFIX}_{part_type}_{slot}"
            uploaded_file = files.get(file_field)
            if not uploaded_file:
                errors[file_field] = f"{label} photo is required."
                continue

            try:
                validate_uploaded_photo(uploaded_file)
            except ValidationError as exc:
                errors[file_field] = exc.messages[0]
            photos.append((slot, uploaded_file))

        payload["items"].append(
            {
                "part_type": part_type,
                "airpods_model": model,
                "model_number": model_number,
                "condition": condition,
                "asking_price_eur": price,
                "cleaned_and_ready": cleaned_and_ready,
                "photos": photos,
            }
        )

    return payload, errors


@transaction.atomic
def save_seller_submission_payload(payload):
    submission = SellerSubmission.objects.create(**payload["submission"])

    for item_payload in payload["items"]:
        photos = item_payload.pop("photos")
        item = SellerSubmissionItem.objects.create(submission=submission, **item_payload)
        for slot, uploaded_file in photos:
            SellerSubmissionItemPhoto.objects.create(item=item, slot=slot, image=uploaded_file)

    return submission
