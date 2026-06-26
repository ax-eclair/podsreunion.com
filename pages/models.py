from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class AirPodsModel(models.Model):
    class Kind(models.TextChoices):
        EARBUDS = "earbuds", "Earbuds"
        CASE = "case", "Charging case"

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    kind = models.CharField(max_length=16, choices=Kind.choices)
    image_path = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Static asset path, for example assets/airpods/products/web/airpods-pro-2-earbuds.png."
        ),
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["kind", "sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SellerSubmission(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWING = "reviewing", "Reviewing"
        COMPLETED = "completed", "Completed"

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    seller_name = models.CharField(max_length=120)
    contact_email = models.EmailField()
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=32)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    shipping_possible = models.BooleanField(default=False)
    local_handoff_possible = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]

    @property
    def full_address(self):
        return ", ".join(
            part
            for part in [self.street_address, self.postal_code, self.city, self.country]
            if part
        )

    def __str__(self):
        return f"{self.seller_name} ({self.contact_email})"


class SellerSubmissionItem(models.Model):
    class PartType(models.TextChoices):
        LEFT = "left", "Left AirPod"
        RIGHT = "right", "Right AirPod"
        CASE = "case", "Charging case"

    class Condition(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"
        DAMAGED = "damaged", "Damaged"
        NOT_SURE = "not-sure", "Not sure yet"

    class ReviewStatus(models.TextChoices):
        NEW = "new", "New"
        REVIEWING = "reviewing", "Reviewing"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    submission = models.ForeignKey(SellerSubmission, related_name="items", on_delete=models.CASCADE)
    part_type = models.CharField(max_length=12, choices=PartType.choices)
    airpods_model = models.ForeignKey(
        AirPodsModel, on_delete=models.PROTECT, related_name="submission_items"
    )
    model_number = models.CharField(max_length=40)
    condition = models.CharField(max_length=16, choices=Condition.choices)
    asking_price_eur = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    cleaned_and_ready = models.BooleanField(default=False)
    review_status = models.CharField(
        max_length=16,
        choices=ReviewStatus.choices,
        default=ReviewStatus.NEW,
    )
    review_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["submission", "part_type"]
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "part_type"],
                name="unique_part_type_per_seller_submission",
            )
        ]

    def __str__(self):
        return f"{self.get_part_type_display()} - {self.airpods_model}"


def seller_submission_photo_upload_to(instance, filename):
    return (
        f"seller-submissions/{instance.item.submission_id}/"
        f"{instance.item.part_type}/{instance.slot}/{filename}"
    )


class SellerSubmissionItemPhoto(models.Model):
    item = models.ForeignKey(SellerSubmissionItem, related_name="photos", on_delete=models.CASCADE)
    slot = models.CharField(max_length=40)
    image = models.FileField(upload_to=seller_submission_photo_upload_to)
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["item", "slot"]
        constraints = [
            models.UniqueConstraint(
                fields=["item", "slot"],
                name="unique_photo_slot_per_seller_submission_item",
            )
        ]

    def __str__(self):
        return f"{self.item} - {self.slot}"
