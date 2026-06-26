from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import (
    CONDITION_LABELS,
    PART_TYPE_LABELS,
    PHOTO_SLOTS,
    save_seller_submission_payload,
    validate_seller_submission_request,
)
from .models import AirPodsModel, SellerSubmissionItem


def home(request):
    return render(request, "pages/index.html")


def impressum(request):
    return render(request, "pages/impressum.html")


def datenschutz(request):
    return render(request, "pages/datenschutz.html")


class SellerSubmissionView(TemplateView):
    template_name = "pages/seller_submission.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._base_context())
        context["submission_saved"] = self.request.session.pop("seller_submission_saved", False)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get("company_website"):
            request.session["seller_submission_saved"] = True
            return redirect("seller_submission")

        payload, errors = validate_seller_submission_request(request.POST, request.FILES)
        if errors:
            context = self.get_context_data()
            context["errors"] = errors
            context["form_data"] = request.POST
            context["selected_parts"] = request.POST.getlist("parts")
            return self.render_to_response(context, status=200)

        save_seller_submission_payload(payload)
        request.session["seller_submission_saved"] = True
        return redirect("seller_submission")

    def _base_context(self):
        earbud_models = AirPodsModel.objects.filter(kind=AirPodsModel.Kind.EARBUDS, is_active=True)
        case_models = AirPodsModel.objects.filter(kind=AirPodsModel.Kind.CASE, is_active=True)
        parts = []
        for value, label in SellerSubmissionItem.PartType.choices:
            parts.append(
                {
                    "value": value,
                    "label": label,
                    "models": case_models
                    if value == SellerSubmissionItem.PartType.CASE
                    else earbud_models,
                    "slots": PHOTO_SLOTS[value],
                }
            )

        return {
            "parts": parts,
            "condition_choices": SellerSubmissionItem.Condition.choices,
            "condition_labels": CONDITION_LABELS,
            "part_type_labels": PART_TYPE_LABELS,
            "selected_parts": [],
            "errors": {},
            "form_data": {},
        }
