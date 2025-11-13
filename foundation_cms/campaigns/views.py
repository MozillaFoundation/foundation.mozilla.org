import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .models.petition import Petition


@require_http_methods(["POST"])
def petition_submit(request):
    """Process petition submission"""
    try:
        petition_id = request.POST.get("petition_id")
        if not petition_id:
            return JsonResponse({"success": False, "message": _("Invalid petition.")}, status=400)

        petition = get_object_or_404(Petition, id=petition_id)

        # Extract form data
        form_data = {
            "email": request.POST.get("email", "").strip(),
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "country": request.POST.get("country", "").strip(),
            "postal_code": request.POST.get("postal_code", "").strip(),
            "comment": request.POST.get("comment", "").strip(),
            "newsletter": request.POST.get("newsletter", "mozilla-foundation"),
            "privacy": request.POST.get("privacy") == "on",
            "email_subscription": request.POST.get("email_subscription") == "on",
        }

        # Basic validation
        if not form_data["email"] or not form_data["privacy"]:
            return JsonResponse(
                {"success": False, "message": _("Please fill in required fields and agree to privacy notice.")},
                status=400,
            )

        # TODO: Submit to our newsletter/CRM system
        # For now, just return success
        success = process_petition_signup(form_data)

        if success:
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Thank you for signing!"),
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("Error processing submission. Please try again.")}, status=500
            )

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": _("Error processing submission. Please try again.")}, status=500
        )


def process_petition_signup(form_data):
    """Process the petition signup - integrate with your newsletter system"""
    try:
        # TODO: Integrate with our existing newsletter signup system
        # This could use our existing newsletter_signup_block logic
        # or integrate with CaMo/Basket/Salesforce

        print(f"Processing petition signup for: {form_data['email']}")

        # For development, return True
        # In production, implement actual integration
        return True

    except Exception as e:
        print(f"Petition signup error: {e}")
        return False
