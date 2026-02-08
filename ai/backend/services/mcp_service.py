import httpx
import asyncio
import os
from typing import Dict, Any, List, Optional


class MCPService:
    """Service for interacting with Fi Money's MCP Server via GCP Functions."""
    
    def __init__(self):
        self.base_url = "https://us-central1-hackathon-62355.cloudfunctions.net"
        self.phone_number = os.getenv("PHONE_NUMBER", "9999999999")
        self.timeout = 30.0
    
    async def fetch_financial_data(self, phone_number: str = None, data_types: List[str] = None) -> Dict[str, Any]:
        """Fetch financial data from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Call your existing GCP function
                response = await client.post(
                    f"{self.base_url}/getBankTransactions",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Error fetching financial data: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"Error in MCP service: {e}")
            return {}
    
    async def fetch_bank_transactions(self, phone_number: str = None) -> List[Dict[str, Any]]:
        """Fetch bank transactions from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                response = await client.post(
                    f"{self.base_url}/getBankTransactions",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "data" in data:
                        return data["data"].get("transactions", [])
                    return []
                else:
                    print(f"Error fetching bank transactions: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Error fetching bank transactions: {e}")
            return []
    
    async def fetch_credit_report(self, phone_number: str = None) -> Dict[str, Any]:
        """Fetch credit report from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                response = await client.post(
                    f"{self.base_url}/getCreditReport",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "data" in data:
                        return data["data"]
                    return {}
                else:
                    print(f"Error fetching credit report: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"Error fetching credit report: {e}")
            return {}
    
    async def fetch_epf_details(self, phone_number: str = None) -> Dict[str, Any]:
        """Fetch EPF details from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                response = await client.post(
                    f"{self.base_url}/getEPFDetails",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "data" in data:
                        return data["data"]
                    return {}
                else:
                    print(f"Error fetching EPF details: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"Error fetching EPF details: {e}")
            return {}
    
    async def fetch_mf_transactions(self, phone_number: str = None) -> List[Dict[str, Any]]:
        """Fetch mutual fund transactions from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                response = await client.post(
                    f"{self.base_url}/getMFTransactions",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "data" in data:
                        return data["data"].get("transactions", [])
                    return []
                else:
                    print(f"Error fetching MF transactions: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"Error fetching MF transactions: {e}")
            return []
    
    async def fetch_net_worth(self, phone_number: str = None) -> Dict[str, Any]:
        """Fetch net worth data from MCP Server."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            
            async with httpx.AsyncClient(timeout=self.timeout, verify=False) as client:
                response = await client.post(
                    f"{self.base_url}/getNetWorth",
                    params={"phoneNumber": user_phone}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "data" in data:
                        return data["data"]
                    return {}
                else:
                    print(f"Error fetching net worth: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"Error fetching net worth: {e}")
            return {}
    
    async def get_comprehensive_financial_data(self, phone_number: str = None) -> Dict[str, Any]:
        """Get comprehensive financial data from all sources."""
        try:
            # Use provided phone number or fallback to default
            user_phone = phone_number or self.phone_number
            print(f"🔍 Debug: Fetching financial data for phone: {user_phone}")
            
            # Fetch all financial data concurrently
            tasks = [
                self.fetch_bank_transactions(user_phone),
                self.fetch_credit_report(user_phone),
                self.fetch_epf_details(user_phone),
                self.fetch_mf_transactions(user_phone),
                self.fetch_net_worth(user_phone)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            bank_transactions, credit_report, epf_details, mf_transactions, net_worth = results
            
            # Handle exceptions
            if isinstance(bank_transactions, Exception):
                bank_transactions = []
            if isinstance(credit_report, Exception):
                credit_report = {}
            if isinstance(epf_details, Exception):
                epf_details = {}
            if isinstance(mf_transactions, Exception):
                mf_transactions = []
            if isinstance(net_worth, Exception):
                net_worth = {}
            
            return {
                "phone_number": user_phone,
                "bank_transactions": bank_transactions,
                "credit_report": credit_report,
                "epf_details": epf_details,
                "mf_transactions": mf_transactions,
                "net_worth": net_worth,
                "timestamp": asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            print(f"Error getting comprehensive financial data: {e}")
            return {
                "phone_number": user_phone,
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            } 