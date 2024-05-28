import requests
import threading

lookup = ""
state = ""
country = ""
url = "https://oic-ajover-desarrollo-axyh19yueizn-ia.integration.ocp.oraclecloud.com/ic/api/integration/v1/flows/rest/ERP_AR_EXT011_LOOKUP_VALUES/1.0/getLookups"

data = {
    "lookup": lookup,
    "country": country,
    "state": state
}

headers = {
    "Authorization" : "Basic SURSVXNlcjoqQWpvdmVyMjAyM2Qq"
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
    threads = []
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
    
    def request(data_lookups, index):
        response = requests.post(url, json=data_lookups, headers=headers)
        response_json = response.json()
        values = response_json.get("values", [])
        results[index] = values
    
    for i, object_datas in enumerate(object_data_lookups):
        thread = threading.Thread(target=request, args=(object_datas, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    account_set_name = account.get("SetName")
    setname_result = results[0]
    if setname_result and account_set_name not in setname_result:
        messages_error.append(f"El valor '{account_set_name}' no existe en la lista de valores de SetName.")
        
    account_vendedor = account.get("Vendedor")
    vendedor_result = results[1]
    if vendedor_result and account_vendedor not in vendedor_result:
        messages_error.append(f"El valor '{account_vendedor}' no existe en la lista de valores de Vendedor.")
    
    condicion_de_flete = account.get("CondicionesDeFlete")
    condicion_de_flete_result = results[2]
    if condicion_de_flete_result and condicion_de_flete not in condicion_de_flete_result:
        messages_error.append(f"El valor '{condicion_de_flete}' no existe en la lista de valores de CondicionesDeFlete.")
        
    customer_class_account = account.get("CustomerClassCode")
    customer_class_result = results[3]
    if customer_class_result and customer_class_account not in customer_class_result:
        messages_error.append(f"El valor '{customer_class_account}' no existe en la lista de valores de CustomerClassCode.")
        
    group_clientes_account = account.get("GrupoClientes")
    group_clientes_result = results[4]
    if group_clientes_result and group_clientes_account in group_clientes_result:
        messages_error.append(f"El valor '{group_clientes_account}' no existe en la lista de valores de GrupoClientes.")
        
    tipo_transporte_account = account.get("TipoDeTransporte")
    tipo_transporte_result = results[5]
    if tipo_transporte_result and tipo_transporte_account in tipo_transporte_result:
        messages_error.append(f"El valor '{tipo_transporte_account}' no existe en la lista de valores de TipoDeTransporte.")
    
    return messages_error
    
