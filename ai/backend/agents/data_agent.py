import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent
from models.agent_messages import AgentCapability
from models.financial_data import ComprehensiveFinancialData, FinancialProfile
from services.mcp_service import MCPService


class DataAgent(BaseAgent):
    """Specialized agent for financial data aggregation and processing."""
    
    def __init__(self):
        super().__init__(
            agent_id="data_agent",
            name="Data Agent",
            description="Specialized in financial data aggregation, validation, and profile compilation",
            specialties=[
                "Financial data aggregation",
                "Data quality validation",
                "Context compilation",
                "Real-time data updates",
                "Profile compilation",
                "Data source management"
            ],
            temperature=0.1,  # Very low temperature for precise data processing
            max_tokens=2000
        )
        self.mcp_service = MCPService()
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for data processing."""
        return """
# Data Agent - Financial Data Processing Specialist

## ROLE DEFINITION
You are a specialized Data Agent responsible for aggregating, validating, and processing financial data from multiple sources. Your expertise covers:

- **Data Aggregation**: Collecting data from multiple financial sources
- **Data Validation**: Ensuring accuracy and completeness of financial data
- **Profile Compilation**: Creating comprehensive financial profiles
- **Context Building**: Providing rich context for analysis
- **Quality Assurance**: Maintaining data integrity and reliability

## CORE PRINCIPLES
1. **Data Accuracy**: Ensure all financial data is accurate and up-to-date
2. **Completeness**: Gather comprehensive data from all available sources
3. **Validation**: Cross-validate data across different sources
4. **Privacy**: Maintain strict data privacy and security standards
5. **Real-time Updates**: Provide current and relevant financial information

## DATA SOURCES
- **Bank Transactions**: Income, expenses, and cash flow patterns
- **Credit Reports**: Credit score, debt levels, and payment history
- **Investment Data**: Mutual funds, stocks, and other investments
- **Retirement Accounts**: EPF, pension, and long-term savings
- **Net Worth**: Comprehensive asset and liability summary

## PROCESSING FRAMEWORK
1. **Data Collection**: Gather data from all available sources
2. **Validation**: Check for accuracy and completeness
3. **Processing**: Calculate derived metrics and ratios
4. **Compilation**: Create comprehensive financial profile
5. **Context Building**: Add relevant context and insights
6. **Quality Check**: Ensure data meets quality standards
"""
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "data_aggregation",
            "data_validation",
            "profile_compilation",
            "context_building",
            "quality_assurance"
        ]
    
    async def compile_financial_profile(self, phone_number: str) -> ComprehensiveFinancialData:
        """Compile comprehensive financial profile from all data sources."""
        try:
            # Fetch all financial data concurrently
            tasks = [
                self.mcp_service.fetch_bank_transactions(phone_number),
                self.mcp_service.fetch_credit_report(phone_number),
                self.mcp_service.fetch_epf_details(phone_number),
                self.mcp_service.fetch_mf_transactions(phone_number),
                self.mcp_service.fetch_net_worth(phone_number)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            bank_transactions, credit_report, epf_details, mf_transactions, net_worth = self._process_results(results)
            
            # Create comprehensive financial data
            financial_data = ComprehensiveFinancialData(
                phone_number=phone_number,
                bank_transactions=bank_transactions,
                credit_report=credit_report,
                epf_details=epf_details,
                mf_transactions=mf_transactions,
                net_worth=net_worth,
                timestamp=datetime.utcnow()
            )
            
            return financial_data
            
        except Exception as e:
            print(f"Error compiling financial profile: {e}")
            return self._create_empty_financial_data(phone_number)
    
    def _process_results(self, results: List) -> tuple:
        """Process results from concurrent data fetching."""
        processed_results = []
        
        for result in results:
            if isinstance(result, Exception):
                print(f"Error in data fetching: {result}")
                processed_results.append(self._get_empty_result_for_type(result))
            else:
                try:
                    # Validate and clean the data
                    processed_results.append(self._validate_and_clean_data(result))
                except Exception as e:
                    print(f"Error processing data: {e}")
                    processed_results.append(self._get_empty_result_for_type(e))
        
        return tuple(processed_results)
    
    def _validate_and_clean_data(self, data: Any) -> Any:
        """Validate and clean data to match expected format."""
        if isinstance(data, list):
            # Clean bank transactions
            cleaned_transactions = []
            for transaction in data:
                try:
                    # Handle missing or invalid transaction types/modes
                    if 'type' in transaction:
                        if transaction['type'] not in ['CREDIT', 'DEBIT', 'INSTALLMENT', 'INTEREST', 'OTHERS']:
                            transaction['type'] = 'OTHERS'
                    if 'mode' in transaction:
                        if transaction['mode'] not in ['UPI', 'CARD_PAYMENT', 'CASH', 'FT', 'ATM', 'NEFT', 'IMPS', 'ACH', 'BILLPAY', 'CHARGES', 'INTEREST', 'INSTALLMENT', 'OTHERS']:
                            transaction['mode'] = 'OTHERS'
                    cleaned_transactions.append(transaction)
                except Exception as e:
                    print(f"Error cleaning transaction: {e}")
                    continue
            return cleaned_transactions
        elif isinstance(data, dict):
            # Clean credit report
            if 'creditScore' in data and data['creditScore'] is None:
                data['creditScore'] = 0
            if 'totalAccounts' not in data:
                data['totalAccounts'] = "0"
            if 'activeAccounts' not in data:
                data['activeAccounts'] = "0"
            if 'accounts' not in data:
                data['accounts'] = []
            return data
        return data
    
    def _get_empty_result_for_type(self, exception: Exception) -> Any:
        """Get empty result based on exception type."""
        # This is a simplified implementation
        # In practice, you'd want to return appropriate empty structures
        return []
    
    def _create_empty_financial_data(self, phone_number: str) -> ComprehensiveFinancialData:
        """Create empty financial data when compilation fails."""
        from models.financial_data import CreditReport, EPFDetails, NetWorth
        
        return ComprehensiveFinancialData(
            phone_number=phone_number,
            bank_transactions=[],
            credit_report=CreditReport(creditScore=0, accounts=[], totalAccounts="0", activeAccounts="0"),
            epf_details=EPFDetails(totalBalance=0, employeeShare=0, employerShare=0, pensionBalance=0),
            mf_transactions=[],
            net_worth=NetWorth(totalNetWorth=0, formattedTotalNetWorth="₹0"),
            timestamp=datetime.utcnow()
        )
    
    async def process_financial_profile(self, financial_data: ComprehensiveFinancialData) -> FinancialProfile:
        """Process raw financial data into structured financial profile."""
        try:
            # Extract and calculate key metrics
            income_analysis = self._analyze_income(financial_data)
            expense_analysis = self._analyze_expenses(financial_data)
            asset_analysis = self._analyze_assets(financial_data)
            debt_analysis = self._analyze_debt(financial_data)
            investment_analysis = self._analyze_investments(financial_data)
            risk_analysis = self._analyze_risk(financial_data)
            
            # Create comprehensive financial profile
            profile = FinancialProfile(
                # Income Analysis
                monthly_income=income_analysis["monthly_income"],
                income_stability=income_analysis["stability"],
                income_source=income_analysis["source"],
                
                # Expense Analysis
                monthly_expenses=expense_analysis["monthly_expenses"],
                expense_categories=expense_analysis["categories"],
                discretionary_income=expense_analysis["discretionary_income"],
                
                # Asset Analysis
                total_assets=asset_analysis["total_assets"],
                liquid_savings=asset_analysis["liquid_savings"],
                investments=asset_analysis["investments"],
                retirement_savings=asset_analysis["retirement_savings"],
                
                # Debt Analysis
                total_debt=debt_analysis["total_debt"],
                credit_score=debt_analysis["credit_score"],
                debt_to_income_ratio=debt_analysis["debt_to_income_ratio"],
                
                # Investment Analysis
                portfolio_value=investment_analysis["portfolio_value"],
                investment_schemes=investment_analysis["schemes"],
                portfolio_performance=investment_analysis["performance"],
                
                # Risk Analysis
                emergency_fund_adequacy=risk_analysis["emergency_fund_adequacy"],
                insurance_coverage=risk_analysis["insurance_coverage"],
                financial_stability_score=risk_analysis["stability_score"]
            )
            
            return profile
            
        except Exception as e:
            print(f"Error processing financial profile: {e}")
            return self._create_empty_financial_profile()
    
    def _analyze_income(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze income from bank transactions."""
        transactions = financial_data.bank_transactions
        
        # Handle different transaction structures
        if not transactions:
            return {
                "monthly_income": 0,
                "stability": "no_data",
                "source": "No income data available"
            }
        
        # Try to find salary transactions
        salary_transactions = []
        credit_transactions = []
        
        for txn in transactions:
            # Handle different transaction structures
            if isinstance(txn, dict):
                narration = txn.get('narration', '').upper()
                txn_type = txn.get('type', '')
                amount = txn.get('amount', 0)
            else:
                # Assume object with attributes
                narration = getattr(txn, 'narration', '').upper()
                txn_type = getattr(txn, 'type', '')
                amount = getattr(txn, 'amount', 0)
            
            if "SALARY" in narration or "SALARY FROM" in narration:
                salary_transactions.append({'amount': amount, 'narration': narration})
            elif txn_type == "CREDIT":
                credit_transactions.append({'amount': amount, 'narration': narration})
        
        if salary_transactions:
            # Use the most recent salary transaction
            latest_salary = max(salary_transactions, key=lambda x: x['amount'])
            monthly_income = latest_salary['amount']
            income_source = latest_salary['narration']
        elif credit_transactions:
            # Estimate from credit transactions
            total_credit = sum(txn['amount'] for txn in credit_transactions)
            monthly_income = total_credit / len(credit_transactions) if credit_transactions else 0
            income_source = "Estimated from transaction patterns"
        else:
            monthly_income = 0
            income_source = "No income data available"
        
        return {
            "monthly_income": monthly_income,
            "stability": "stable" if salary_transactions else "estimated",
            "source": income_source
        }
    
    def _analyze_expenses(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze expenses from bank transactions."""
        transactions = financial_data.bank_transactions
        
        if not transactions:
            return {
                "monthly_expenses": 0,
                "categories": {},
                "discretionary_income": 0
            }
        
        # Calculate total expenses
        debit_transactions = []
        for txn in transactions:
            if isinstance(txn, dict):
                txn_type = txn.get('type', '')
                amount = txn.get('amount', 0)
            else:
                txn_type = getattr(txn, 'type', '')
                amount = getattr(txn, 'amount', 0)
            
            if txn_type == "DEBIT":
                debit_transactions.append({'amount': amount, 'narration': txn.get('narration', '') if isinstance(txn, dict) else getattr(txn, 'narration', '')})
        
        total_expenses = sum(txn['amount'] for txn in debit_transactions)
        
        # Categorize expenses
        categories = self._categorize_expenses(debit_transactions)
        
        # Calculate discretionary income
        income_analysis = self._analyze_income(financial_data)
        monthly_income = income_analysis["monthly_income"]
        discretionary_income = monthly_income - total_expenses
        
        return {
            "monthly_expenses": total_expenses,
            "categories": categories,
            "discretionary_income": discretionary_income
        }
    
    def _categorize_expenses(self, transactions: List) -> Dict[str, float]:
        """Categorize expenses based on transaction descriptions."""
        categories = {
            "food_delivery": 0,
            "transport": 0,
            "utilities": 0,
            "entertainment": 0,
            "shopping": 0,
            "healthcare": 0,
            "education": 0,
            "others": 0
        }
        
        for txn in transactions:
            if isinstance(txn, dict):
                narration = txn.get('narration', '').lower()
                amount = txn.get('amount', 0)
            else:
                narration = getattr(txn, 'narration', '').lower()
                amount = getattr(txn, 'amount', 0)
            
            if any(keyword in narration for keyword in ["swiggy", "zomato", "food", "restaurant"]):
                categories["food_delivery"] += amount
            elif any(keyword in narration for keyword in ["uber", "ola", "petrol", "fuel"]):
                categories["transport"] += amount
            elif any(keyword in narration for keyword in ["electricity", "water", "gas", "broadband"]):
                categories["utilities"] += amount
            elif any(keyword in narration for keyword in ["movie", "netflix", "amazon", "flipkart"]):
                categories["entertainment"] += amount
            elif any(keyword in narration for keyword in ["medical", "pharmacy", "hospital"]):
                categories["healthcare"] += amount
            elif any(keyword in narration for keyword in ["school", "college", "course"]):
                categories["education"] += amount
            else:
                categories["others"] += amount
        
        return categories
    
    def _analyze_assets(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze assets from net worth data."""
        net_worth = financial_data.net_worth
        assets = net_worth.assets if hasattr(net_worth, 'assets') else []
        
        total_assets = sum(asset.value for asset in assets)
        
        # Categorize assets
        liquid_savings = 0
        investments = 0
        retirement_savings = 0
        
        for asset in assets:
            if "SAVINGS" in asset.type:
                liquid_savings += asset.value
            elif "MUTUAL_FUND" in asset.type or "SECURITIES" in asset.type:
                investments += asset.value
            elif "EPF" in asset.type:
                retirement_savings += asset.value
        
        return {
            "total_assets": total_assets,
            "liquid_savings": liquid_savings,
            "investments": investments,
            "retirement_savings": retirement_savings
        }
    
    def _analyze_debt(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze debt from credit report."""
        credit_report = financial_data.credit_report
        
        total_debt = sum(account.currentBalance for account in credit_report.accounts)
        credit_score = credit_report.creditScore
        
        # Calculate debt-to-income ratio
        income_analysis = self._analyze_income(financial_data)
        monthly_income = income_analysis["monthly_income"]
        debt_to_income_ratio = total_debt / (monthly_income * 12) if monthly_income > 0 else 0
        
        return {
            "total_debt": total_debt,
            "credit_score": credit_score,
            "debt_to_income_ratio": debt_to_income_ratio
        }
    
    def _analyze_investments(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze investments from mutual fund transactions."""
        mf_transactions = financial_data.mf_transactions
        
        portfolio_value = sum(txn.amount for txn in mf_transactions)
        schemes = len(set(txn.schemeName for txn in mf_transactions))
        
        # Simple performance assessment
        if portfolio_value > 0:
            performance = "good" if portfolio_value > 50000 else "moderate"
        else:
            performance = "no_investments"
        
        return {
            "portfolio_value": portfolio_value,
            "schemes": schemes,
            "performance": performance
        }
    
    def _analyze_risk(self, financial_data: ComprehensiveFinancialData) -> Dict[str, Any]:
        """Analyze risk factors."""
        # Analyze emergency fund adequacy
        asset_analysis = self._analyze_assets(financial_data)
        expense_analysis = self._analyze_expenses(financial_data)
        
        liquid_savings = asset_analysis["liquid_savings"]
        monthly_expenses = expense_analysis["monthly_expenses"]
        
        months_coverage = liquid_savings / monthly_expenses if monthly_expenses > 0 else 0
        
        if months_coverage >= 6:
            emergency_fund_adequacy = "adequate"
        elif months_coverage >= 3:
            emergency_fund_adequacy = "moderate"
        else:
            emergency_fund_adequacy = "insufficient"
        
        # Simple insurance coverage assessment
        insurance_coverage = "unknown"  # Would need insurance data
        
        # Calculate financial stability score
        debt_analysis = self._analyze_debt(financial_data)
        debt_to_income_ratio = debt_analysis["debt_to_income_ratio"]
        credit_score = debt_analysis["credit_score"]
        
        # Simple stability score (0-1)
        stability_score = 0.5  # Base score
        if credit_score > 700:
            stability_score += 0.2
        if debt_to_income_ratio < 0.3:
            stability_score += 0.2
        if months_coverage >= 3:
            stability_score += 0.1
        
        return {
            "emergency_fund_adequacy": emergency_fund_adequacy,
            "insurance_coverage": insurance_coverage,
            "stability_score": min(stability_score, 1.0)
        }
    
    def _create_empty_financial_profile(self) -> FinancialProfile:
        """Create empty financial profile when processing fails."""
        return FinancialProfile(
            monthly_income=0,
            income_stability="unknown",
            income_source="unknown",
            monthly_expenses=0,
            expense_categories={},
            discretionary_income=0,
            total_assets=0,
            liquid_savings=0,
            investments=0,
            retirement_savings=0,
            total_debt=0,
            credit_score=0,
            debt_to_income_ratio=0,
            portfolio_value=0,
            investment_schemes=0,
            portfolio_performance="unknown",
            emergency_fund_adequacy="unknown",
            insurance_coverage="unknown",
            financial_stability_score=0
        ) 