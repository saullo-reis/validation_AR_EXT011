import threading
import requests
import os
from dotenv import load_dotenv

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

def contact_points_lookup():
    results = [None] * 7
    
    object_data_lookups = [
        {"lookup":"COMMUNICATION_TYPE"},
        {"lookup":"PHONE_LINE_TYPE"},
        {"lookup":"CONTACT_POINT_PURPOSE"},
        {"lookup":"AJ_PHONE_COUNTRY"},
        {"lookup":"HZ_INSTANT_MESSENGER_TYPE"},
        {"lookup":"EMAIL_FORMAT"},
        {"lookup":"HZ_URL_TYPES"}
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
    return results

def account_lookup():
    results = [None] * 6
    
    object_data_lookups = [
        {"lookup": "AJ_SETNAME"},
        {"lookup": "AJ_MEMBER_PERSON"},
        {"lookup": "AJ_FREIGHT_TERMS"},
        {"lookup": "CUSTOMER CLASS"},
        {"lookup": "PRICE_G_CLIENTES"},
        {"lookup": "AJ_CARRIER_ID"}
    ]
    threads = []
    
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
    return results

def address_lookup(address):
    results = [None] * 5
    
    object_data_lookups = [
        {"lookup":"PAISES"},
        {"lookup":"AJ_STATE", "country": "CO"},
        {"lookup":"AJ_CITY", "state": "RJ"},
        {"lookup":"AJ_LANGUAGES"},
        {"lookup":"SITE_USE_CODE"}
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
        
    return results

def contact_lookup():
    results = [None] * 3
    
    object_data_lookups = [
        {"lookup":"ORA_PSC_CC_CONTACT_TITLE"},
        {"lookup":"RESPONSIBILITY"},
        {"lookup":"SITE_USE_CODE"}
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
        
    return results
    
def profile_lookup():
    results = [None] * 6
    
    object_data_lookups = [
        {"lookup":"AJ_CURRENCY_CODE"},
        {"lookup":"AR_CMGT_CREDIT_CLASSIFICATION"},
        {"lookup":"AJ_PAYMENT_TERMS"},
        {"lookup":"RISK_CODE"},
        {"lookup":"AJ_GROUP_RULES"},
        {"lookup":"AJ_HOLD_REASON"}
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
        
    return results

