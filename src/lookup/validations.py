import requests
import threading
from dotenv import load_dotenv
import os

current_directory = os.path.dirname(__file__)
dotenv_path = os.path.abspath(os.path.join(current_directory, '..', '..', '.env'))
load_dotenv(dotenv_path)

lookup = ""
state = ""
country = ""
url = "https://oic-ajover-desarrollo-axyh19yueizn-ia.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/ERP_AR_EXT011_LOOKUP_VALUES/1.0/getLookups"
auth = os.getenv("AUTH")


data = {
    "lookup": lookup,
    "country": country,
    "state": state
}

headers = {
    "Authorization" : auth
}

def verify_lookups_organization(organization):
    messages_error = []
    
    tipo_identificacion = organization.get("RegistrationTypeCode")
    if tipo_identificacion:
        data = {"lookup": "AJOVER_TIPO_IDENTIFICACION"}
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        values = response_json.get("values", [])
        if tipo_identificacion not in values:
            messages_error.append(f"El valor '{tipo_identificacion}' no existe en la lista de valores de RegistrationTypeCode.")
            
    tipo_persona = organization.get("TipoPersona")
    if tipo_persona:
        if tipo_persona not in ["J", "N", "N/A"]:
            messages_error.append(f"El valor '{tipo_persona}' no existe en la lista de valores de TipoPersona.")
            
    tipo_persona_juridica = organization.get("TipoPersonaJuridica")
    if tipo_persona_juridica:
        if tipo_persona_juridica not in ["COOP", "AGRM", "FUND", "SAS", "LTDA", "SA", "COMS", "COMA", "COTB", "N/D"]:
            messages_error.append(f"El valor '{tipo_persona_juridica}' no existe en la lista de valores de TipoPersonaJuridica.")
    
    return messages_error

def verify_lookups_account(account):
    messages_error = []
    results = [None] * 6
    
    object_data_lookups = [
        {"lookup": "AJ_SETNAME"},
        {"lookup": "AJ_MEMBER_PERSON"},
        {"lookup": "AJ_FREIGHT_TERMS"},
        {"lookup": "CUSTOMER CLASS"},
        {"lookup": "PRICE_G_CLIENTES"},
        {"lookup": "AJ_CARRIER_ID"}
    ]
    
    account_fields = [
        ("SetName", "AJ_SETNAME", 0),
        ("Vendedor", "AJ_MEMBER_PERSON", 1),
        ("CondicionesDeFlete", "AJ_FREIGHT_TERMS", 2),
        ("CustomerClassCode", "CUSTOMER CLASS", 3),
        ("GrupoClientes", "PRICE_G_CLIENTES", 4),
        ("TipoDeTransporte", "AJ_CARRIER_ID", 5)
    ]
    
    def request(data_lookups, index):
        response = requests.post(url, json=data_lookups, headers=headers)
        response_json = response.json()
        values = response_json.get("values", [])
        results[index] = values
    
    threads = []
    for i, object_datas in enumerate(object_data_lookups):
        thread = threading.Thread(target=request, args=(object_datas, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
        
    for field, lookup, index in account_fields:
        account_value = account.get(field)
        lookup_result = results[index]
        if account_value is not None and lookup_result and account_value not in lookup_result:
            messages_error.append(f"El valor '{account_value}' no existe en la lista de valores de {field}.")
    
    return messages_error
    

def verify_lookups_compliance(compliance):
    messages_error = []

    def verify_si_or_no(value, field):
        if value not in ["SI", "NO"]:
            messages_error.append(f"{value} no existe en la lista de valores de {field}")

    fields_to_check_si_no = [
        "PersonaExpuestaPublicamente",
        "VinculosConAlguienQueLaboreEnAjoverDarnel",
        "ContrataConElEstado",
        "ManejaRecursosPublicos",
        "CalificacionRiesgosTercero",
        "VinculoConUnaPersonaExpuestaPublicamente",
        "VigiladoSuperCiedades",
        "Otros",
        "MonedaExtranjera"
    ]

    for field in fields_to_check_si_no:
        value = compliance.get(field)
        if value:
            verify_si_or_no(value, field)

    sistemaSeguridadAcreditado = compliance.get("SistemaSeguridadAcreditado")
    if sistemaSeguridadAcreditado and sistemaSeguridadAcreditado not in ["BASC", "CEA", "NA"]:
        messages_error.append(f"{sistemaSeguridadAcreditado} no existe en la lista de valores de SistemaSeguridadAcreditado")
    return messages_error

def verify_lookups_address(address):
    messages_error = []
    results = [None] * 5
    
    object_data_lookups = [
        {"lookup":"PAISES"},
        {"lookup":"AJ_STATE", "country": "CO"},
        {"lookup":"AJ_CITY", "state": "RJ"},
        {"lookup":"AJ_LANGUAGES"},
        {"lookup":"SITE_USE_CODE"}
    ]
    
    address_fields = [
        ("Country", "PAISES", 0),
        ("Province", "AJ_STATE", 1),
        ("City", "AJ_CITY", 2),
        ("Language", "AJ_LANGUAGES", 3),
        ("SiteUseCode", "SITE_USE_CODE", 4),
    ]
    
    def request(data_lookups, index):
        response = requests.post(url, json=data_lookups, headers=headers)
        response_json = response.json()
        values = response_json.get("values", [])
        results[index] = values
    
    threads = []
    for i, object_datas in enumerate(object_data_lookups):
        if object_datas.get("country") and object_datas.get("country") == "CO":
            object_datas["country"] = address["Country"]
        if object_datas.get("state") and object_datas.get("state") == "RJ":
            object_datas["state"] = address["Province"]
        thread = threading.Thread(target=request, args=(object_datas, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
        
    for field, lookup, index in address_fields:
        address_value = address.get(field)
        lookup_result = results[index]
        if address_value is not None and lookup_result and address_value not in lookup_result:
            messages_error.append(f"El valor '{address_value}' no existe en la lista de valores de {field}.")
    
    return messages_error

def verify_lookups_contact(contact):
    messages_error = []
    results = [None] * 3
    
    object_data_lookups = [
        {"lookup":"ORA_PSC_CC_CONTACT_TITLE"},
        {"lookup":"RESPONSIBILITY"},
        {"lookup":"SITE_USE_CODE"}
    ]
    
    contact_fields = [
        ("SalutoryIntroduction", "ORA_PSC_CC_CONTACT_TITLE", 0),
        ("JobTitleCode", "RESPONSIBILITY", 1),
        ("TipoResponsabilidad", "SITE_USE_CODE", 2)
    ]
    
    def request(data_lookups, index):
        response = requests.post(url, json=data_lookups, headers=headers)
        response_json = response.json()
        values = response_json.get("values", [])
        results[index] = values
    
    threads = []
    for i, object_datas in enumerate(object_data_lookups):
        
        thread = threading.Thread(target=request, args=(object_datas, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
        
    for field, lookup, index in contact_fields:
        if field == 'TipoResponsabilidad':
            responsability = contact.get("Responsabilities")
            tiporesponsability = responsability[0].get(field)
            lookup_result = results[index]
            if contact_value is not None and lookup_result and tiporesponsability not in lookup_result:
                messages_error.append(f"El valor '{tiporesponsability}' no existe en la lista de valores de {field}.")
            continue
        contact_value = contact.get(field)
        lookup_result = results[index]
        if contact_value is not None and lookup_result and contact_value not in lookup_result:
            messages_error.append(f"El valor '{contact_value}' no existe en la lista de valores de {field}.")
    
    return messages_error