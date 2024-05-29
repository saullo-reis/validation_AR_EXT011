import io
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from fdk import response
from src.mandatory.validations import (
    verify_fields_mandatories_organization,
    verify_fields_mandatories_account,
    verify_fields_mandatories_address,
    verify_fields_mandatories_compliance,
    verify_fields_mandatories_profile,
    verify_fields_mandatories_email,
    verify_fields_mandatories_http,
    verify_fields_mandatories_instant_messaging,
    verify_fields_mandatories_phone
)

from src.lookup.validations import (
    verify_lookups_organization,
    verify_lookups_account,
    verify_lookups_compliance,
    verify_lookups_address,
    verify_lookups_contact,
    verify_lookups_profile,
    verify_lookups_contact_point
)

from src.lookup.lookup_fields import (
    contact_points_lookup,
    account_lookup,
    address_lookup,
    contact_lookup,
    profile_lookup
)

def handler(ctx, data: io.BytesIO = None):
    try:
        body = json.loads(data.getvalue())
        messages_error = []
        
        with ThreadPoolExecutor() as executor:
            contact_points_lookup_result = executor.submit(contact_points_lookup).result()
            account_lookup_result = executor.submit(account_lookup).result()
            contact_lookup_result = executor.submit(contact_lookup).result()
            profile_lookup_result = executor.submit(profile_lookup).result()
        
        for org in body.get("Organization", []):
            messages_error.extend(verify_fields_mandatories_organization(org))
            messages_error.extend(verify_lookups_organization(org))
            
            for account in org.get("Account", []):
                messages_error.extend(verify_fields_mandatories_account(account))
                messages_error.extend(verify_lookups_account(account, account_lookup_result))
                
                compliance = account.get("Compliance", {})
                if compliance:
                    messages_error.extend(verify_fields_mandatories_compliance(compliance))
                    messages_error.extend(verify_lookups_compliance(compliance))
                    
                for address in account.get("Address", []):
                    messages_error.extend(verify_fields_mandatories_address(address))
                    messages_error.extend(verify_lookups_address(address, address_lookup(address)))
                    
                for profile in account.get("CustomerProfile", []):
                    messages_error.extend(verify_fields_mandatories_profile(profile))
                    messages_error.extend(verify_lookups_profile(profile, profile_lookup_result))
                    
                for contact in account.get("Contact", []):
                    messages_error.extend(verify_lookups_contact(contact, contact_lookup_result))
                    for contact_points in contact.get("ContactPoint"):
                        messages_error.extend(verify_lookups_contact_point(contact_points, contact_points_lookup_result))
                        type_contact = contact_points.get("ContactPointType")
                        if(type_contact == "PHONE"):
                            messages_error.extend(verify_fields_mandatories_phone(contact_points))
                        if(type_contact == "INSTANT_MESSAGING"):
                            messages_error.extend(verify_fields_mandatories_instant_messaging(contact_points))
                        if(type_contact == "WEB"):
                            messages_error.extend(verify_fields_mandatories_http(contact_points))
                        if(type_contact == "EMAIL"):
                            messages_error.extend(verify_fields_mandatories_email(contact_points))
        
        if messages_error:
            return response.Response(
                ctx, response_data=json.dumps({
                    "message": "; ".join(messages_error),
                    "http_code": 400,
                    "data": body
                }),
                headers={"Content-Type": "application/json"}
            )
        else: 
            return response.Response(
                ctx, response_data=json.dumps({
                    "message": "Éxito, Ningún error encontrado en los campos enviados.",
                    "http_code": 200,
                    "data": body
                }),
                headers={"Content-Type": "application/json"}
            )
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
        return response.Response(
            ctx, response_data=json.dumps({
                "type": "Error al analizar los datos JSON.",
                "message": str(ex),
                "http_code": 400,
            }),
            headers={"Content-Type": "application/json"}
        )

 