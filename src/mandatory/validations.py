from src.mandatory.mandatory_fields import (
    FIELDS_MANDATORIES_ORGANIZATION,
    FIELDS_MANDATORIES_ACCOUNT,
    FIELDS_MANDATORIES_COMPLIANCE,
    FIELDS_MANDATORIES_CUSTOMER_PROFILE,
    FIELDS_MANDATORIES_ADDRESS,
    FIELDS_MANDATORIES_CONTACT_POINT_EMAIL,
    FIELDS_MANDATORIES_CONTACT_POINT_HTTP,
    FIELDS_MANDATORIES_CONTACT_POINT_INSTANT_MESSAGING,
    FIELDS_MANDATORIES_CONTACT_POINT_PHONE
)


def verify_fields_mandatories_organization(organization):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_ORGANIZATION.items():
        if field not in organization or not organization[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_account(account):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_ACCOUNT.items():
        if field not in account or not account[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_compliance(compliance):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_COMPLIANCE.items():
        if field not in compliance or not compliance[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_address(address):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_ADDRESS.items():
        if field not in address or not address[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_profile(profile):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_CUSTOMER_PROFILE.items():
        if field not in profile or not profile[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_phone(phone):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_CONTACT_POINT_PHONE.items():
        if field not in phone or not phone[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_instant_messaging(instant_messaging):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_CONTACT_POINT_INSTANT_MESSAGING.items():
        if field not in instant_messaging or not instant_messaging[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_email(email):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_CONTACT_POINT_EMAIL.items():
        if field not in email or not email[field]:
            messages_error.append(message)
    return messages_error

def verify_fields_mandatories_http(http):
    messages_error = []
    for field, message in FIELDS_MANDATORIES_CONTACT_POINT_HTTP.items():
        if field not in http or not http[field]:
            messages_error.append(message)
    return messages_error