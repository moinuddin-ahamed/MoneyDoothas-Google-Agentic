import requests
import json
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

def get_net_worth(phone_number="9999999999"):
    url = "https://us-central1-hackathon-62355.cloudfunctions.net/getNetWorth"
    params = {"phoneNumber": phone_number}
    response = requests.post(url, params=params, verify=False, timeout=30)
    return response.json()

def get_credit_report(phone_number="9999999999"):
    url = "https://us-central1-hackathon-62355.cloudfunctions.net/getCreditReport"
    params = {"phoneNumber": phone_number}
    response = requests.post(url, params=params, verify=False, timeout=30)
    return response.json()

def get_epf_details(phone_number="9999999999"):
    url = "https://us-central1-hackathon-62355.cloudfunctions.net/getEPFDetails"
    params = {"phoneNumber": phone_number}
    response = requests.post(url, params=params, verify=False, timeout=30)
    return response.json()

def get_mf_transactions(phone_number="9999999999"):
    url = "https://us-central1-hackathon-62355.cloudfunctions.net/getMFTransactions"
    params = {"phoneNumber": phone_number}
    response = requests.post(url, params=params, verify=False, timeout=30)
    return response.json()

def get_bank_transactions(phone_number="9999999999"):
    url = "https://us-central1-hackathon-62355.cloudfunctions.net/getBankTransactions"
    params = {"phoneNumber": phone_number}
    response = requests.post(url, params=params, verify=False, timeout=30)
    return response.json()

def get_all_data(phone_number="9999999999"):
    return {
        "net_worth": get_net_worth(phone_number),
        "credit_report": get_credit_report(phone_number),
        "epf_details": get_epf_details(phone_number),
        "mf_transactions": get_mf_transactions(phone_number),
        "bank_transactions": get_bank_transactions(phone_number),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("Testing all functions...")
    
    net_worth = get_net_worth("9999999999")
    print("Net Worth:")
    print(json.dumps(net_worth, indent=2))
    
    credit_report = get_credit_report("9999999999")
    print("\nCredit Report:")
    print(json.dumps(credit_report, indent=2))
    
    epf_details = get_epf_details("9999999999")
    print("\nEPF Details:")
    print(json.dumps(epf_details, indent=2))
    
    mf_transactions = get_mf_transactions("9999999999")
    print("\nMF Transactions:")
    print(json.dumps(mf_transactions, indent=2))
    
    bank_transactions = get_bank_transactions("9999999999")
    print("\nBank Transactions:")
    print(json.dumps(bank_transactions, indent=2))
    
    print("\nDone!") 