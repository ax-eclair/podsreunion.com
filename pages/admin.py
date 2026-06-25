from pathlib import Path

from django.contrib import admin
from django.utils.html import format_html

from .models import AirPodsModel, SellerSubmission, SellerSubmissionItem, SellerSubmissionItemPhoto

PREVIEWABLE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


@admin.register(AirPodsModel)
class AirPodsModelAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "is_active", "sort_order", "image_path")
    list_filter = ("kind", "is_active")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "slug", "image_path")
    prepopulated_fields = {"slug": ("name",)}


class SellerSubmissionItemInline(admin.TabularInline):
    model = SellerSubmissionItem
    extra = 0
    fields = (
        "part_type",
        "airpods_model",
        "condition",
        "asking_price_eur",
        "cleaned_and_ready",
        "review_status",
        "review_notes",
    )
    readonly_fields = (
        "part_type",
        "airpods_model",
        "condition",
        "asking_price_eur",
        "cleaned_and_ready",
    )
    show_change_link = True


@admin.register(SellerSubmission)
class SellerSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "seller_name",
        "contact_email",
        "city",
        "country",
        "status",
        "item_count",
    )
    list_filter = ("status", "shipping_possible", "local_handoff_possible", "country", "created_at")
    search_fields = (
        "seller_name",
        "contact_email",
        "street_address",
        "postal_code",
        "city",
        "country",
        "notes",
    )
    readonly_fields = ("created_at", "full_address")
    inlines = [SellerSubmissionItemInline]
    fieldsets = (
        ("Review", {"fields": ("status",)}),
        (
            "Seller",
            {
                "fields": (
                    "seller_name",
                    "contact_email",
                    "street_address",
                    "postal_code",
                    "city",
                    "country",
                    "full_address",
                )
            },
        ),
        (
            "Options",
            {"fields": ("shipping_possible", "local_handoff_possible", "notes")},
        ),
        ("Metadata", {"fields": ("created_at",)}),
    )

    def item_count(self, obj):
        return obj.items.count()


class SellerSubmissionItemPhotoInline(admin.TabularInline):
    model = SellerSubmissionItemPhoto
    extra = 0
    readonly_fields = ("slot", "image", "uploaded_at", "photo_preview", "download_link")
    fields = ("slot", "image", "photo_preview", "download_link", "uploaded_at")

    def photo_preview(self, obj):
        if not obj.pk or not obj.image:
            return "-"
        extension = Path(obj.image.name).suffix.lower().lstrip(".")
        if extension not in PREVIEWABLE_EXTENSIONS:
            return "Preview unavailable for this file type."
        return format_html(
            '<img src="{}" style="max-width: 180px; max-height: 140px;" alt="">', obj.image.url
        )

    def download_link(self, obj):
        if not obj.pk or not obj.image:
            return "-"
        return format_html('<a href="{}">Download</a>', obj.image.url)


@admin.register(SellerSubmissionItem)
class SellerSubmissionItemAdmin(admin.ModelAdmin):
    list_display = (
        "submission",
        "part_type",
        "airpods_model",
        "condition",
        "asking_price_eur",
        "review_status",
    )
    list_filter = ("part_type", "condition", "review_status", "airpods_model")
    search_fields = (
        "submission__seller_name",
        "submission__contact_email",
        "airpods_model__name",
        "model_number",
        "review_notes",
    )
    readonly_fields = (
        "submission",
        "part_type",
        "airpods_model",
        "model_number",
        "condition",
        "asking_price_eur",
    )
    inlines = [SellerSubmissionItemPhotoInline]


@admin.register(SellerSubmissionItemPhoto)
class SellerSubmissionItemPhotoAdmin(admin.ModelAdmin):
    list_display = ("item", "slot", "uploaded_at", "download_link")
    list_filter = ("slot", "uploaded_at")
    search_fields = (
        "item__submission__seller_name",
        "item__submission__contact_email",
        "item__airpods_model__name",
    )
    readonly_fields = ("uploaded_at", "photo_preview", "download_link")

    def photo_preview(self, obj):
        if not obj.pk or not obj.image:
            return "-"
        extension = Path(obj.image.name).suffix.lower().lstrip(".")
        if extension not in PREVIEWABLE_EXTENSIONS:
            return "Preview unavailable for this file type."
        return format_html(
            '<img src="{}" style="max-width: 240px; max-height: 180px;" alt="">', obj.image.url
        )

    def download_link(self, obj):
        if not obj.pk or not obj.image:
            return "-"
        return format_html('<a href="{}">Download</a>', obj.image.url)
