import datetime
from rest_framework import serializers
from wagtail_airtable.serializers import AirtableSerializer

from networkapi.wagtailpages.fields import ExtendedYesNoField
from networkapi.wagtailpages.pagemodels.products import TRACK_RECORD_CHOICES


class TrackRecordChoicesSerializer(serializers.RelatedField):
    def to_internal_value(self, data):
        value = data.lower().strip()
        for choice_key, choice_value in TRACK_RECORD_CHOICES:
            if choice_key.lower() == value:
                return str(choice_key)
        return data

    def get_queryset(self):
        pass


class ExtendedYesNoSerializer(serializers.RelatedField):
    """
    Custom serializer for importing ExtendedYesNoFields.

    ie. Finds "CD" in a list of ["CD", "Yes", "No", "NA"].
    """

    def to_internal_value(self, data):
        value = data.lower().strip()
        for choice_key, choice_value in ExtendedYesNoField.choice_list:
            if choice_key.lower() == value:
                return choice_key
        return data

    def get_queryset(self):
        pass


class DateSerializer(serializers.DateTimeField):
    def to_internal_value(self, date):
        if type(date) == str and len(date):
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return date


class ProductSerializer(AirtableSerializer):
    """
    The generic serializer for ProductPage's.

    GeneralProductPage and SoftwareProductPage serializers inherit from this class,
    the exact same way the pages do.
    """

    title = serializers.CharField(max_length=255, required=True)
    privacy_ding = serializers.BooleanField(default=False)
    adult_content = serializers.BooleanField(default=False)
    uses_wifi = serializers.BooleanField(default=False)
    uses_bluetooth = serializers.BooleanField(default=False)
    review_date = DateSerializer(required=True)
    company = serializers.CharField(required=False, max_length=100)
    blurb = serializers.CharField(required=False, max_length=5000)
    product_url = serializers.URLField(required=False, max_length=2048)
    price = serializers.CharField(required=False, max_length=100)
    worst_case = serializers.CharField(required=False, max_length=5000)
    signup_requires_email = ExtendedYesNoSerializer(default='CD')
    signup_requires_phone = ExtendedYesNoSerializer(default='CD')
    signup_requires_third_party_account = ExtendedYesNoSerializer(default='CD')
    signup_requirement_explanation = serializers.CharField(required=False, max_length=5000)
    how_does_it_use_data_collected = serializers.CharField(required=False, max_length=5000)
    data_collection_policy_is_bad = serializers.BooleanField(default=False)
    user_friendly_privacy_policy = ExtendedYesNoSerializer(default='CD')
    user_friendly_privacy_policy_helptext = serializers.CharField(required=False, max_length=5000)
    show_ding_for_minimum_security_standards = serializers.BooleanField(default=False)
    meets_minimum_security_standards = serializers.BooleanField(default=False)
    uses_encryption = ExtendedYesNoSerializer(default='CD')
    uses_encryption_helptext = serializers.CharField(required=False, max_length=5000)
    security_updates = ExtendedYesNoSerializer(default='CD')
    security_updates_helptext = serializers.CharField(required=False, max_length=5000)
    strong_password = ExtendedYesNoSerializer(default='CD')
    strong_password_helptext = serializers.CharField(required=False, max_length=5000)
    manage_vulnerabilities = ExtendedYesNoSerializer(default='CD')
    manage_vulnerabilities_helptext = serializers.CharField(required=False, max_length=5000)
    privacy_policy = ExtendedYesNoSerializer(default='CD')
    privacy_policy_helptext = serializers.CharField(required=False, max_length=5000)


class GeneralProductPageSerializer(ProductSerializer):
    """
    General Product Page Serializer is for ingesting data from Airtable and
    validating it to match the import fields from the General Product page
    """

    camera_device = ExtendedYesNoSerializer(default='CD')
    camera_app = ExtendedYesNoSerializer(default='CD')
    microphone_device = ExtendedYesNoSerializer(default='CD')
    microphone_app = ExtendedYesNoSerializer(default='CD')
    location_device = ExtendedYesNoSerializer(default='CD')
    location_app = ExtendedYesNoSerializer(default='CD')
    personal_data_collected = serializers.CharField(required=False, max_length=5000)
    biometric_data_collected = serializers.CharField(required=False, max_length=5000)
    social_data_collected = serializers.CharField(required=False, max_length=5000)
    how_can_you_control_your_data = serializers.CharField(required=False, max_length=5000)
    data_control_policy_is_bad = serializers.BooleanField(default=False, required=False)  # TODO: Test a blank import
    company_track_record = TrackRecordChoicesSerializer(default='Average')  # TODO: Test this imports correctly
    track_record_is_bad = serializers.BooleanField(default=False, required=False)
    track_record_details = serializers.CharField(required=False, max_length=5000)
    offline_capable = ExtendedYesNoSerializer(default='CD')
    offline_use_description = serializers.CharField(required=False, max_length=5000)
    uses_ai = ExtendedYesNoSerializer(default='CD')
    ai_is_transparent = ExtendedYesNoSerializer(default='CD')
    ai_helptext = serializers.CharField(required=False, max_length=5000)


class SoftwareProductPageSerializer(ProductSerializer):
    handles_recordings_how = serializers.CharField(required=False, max_length=5000)
    recording_alert = ExtendedYesNoField(default='CD')
    recording_alert_helptext = serializers.CharField(required=False, max_length=5000)
    medical_privacy_compliant = serializers.BooleanField(default=False)
    medical_privacy_compliant_helptext = serializers.CharField(required=False, max_length=5000)
    host_controls = serializers.CharField(required=False, max_length=5000)
    easy_to_learn_and_use = serializers.BooleanField(default=False)
    easy_to_learn_and_use_helptext = serializers.CharField(required=False, max_length=5000)
