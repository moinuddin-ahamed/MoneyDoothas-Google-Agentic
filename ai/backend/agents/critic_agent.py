import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.base_agent import BaseAgent
from models.agent_messages import (
    AgentMessage, ValidationResult, ValidationStatus, 
    ValidationError, HallucinationFlag, ConfidenceLevel
)
from models.financial_data import ComprehensiveFinancialData, FinancialProfile


class CriticAgent(BaseAgent):
    """Specialized agent for validation, hallucination detection, and quality assurance."""
    
    def __init__(self):
        super().__init__(
            agent_id="critic_agent",
            name="Critic Agent",
            description="Validates recommendations and detects hallucinations for quality assurance",
            specialties=[
                "Recommendation validation",
                "Hallucination detection",
                "Data consistency checking",
                "Logical error identification",
                "Quality assurance",
                "Fact verification"
            ],
            temperature=0.1,  # Very low temperature for precise validation
            max_tokens=3000
        )
    
    def get_prompt_template(self) -> str:
        """Return the specialized prompt template for validation."""
        return """
# Critic Agent - Advanced Validation and Hallucination Detection Specialist

## ROLE DEFINITION
You are a specialized Critic Agent responsible for validating financial recommendations and detecting hallucinations. Your expertise covers:

- **Precision Validation**: Verify every number and calculation against provided data
- **Hallucination Detection**: Identify false claims, unsupported assumptions, and data fabrications
- **Logical Consistency**: Check for internal contradictions and impossible scenarios
- **Data Verification**: Ensure all claims are backed by actual financial data
- **Loop Prevention**: Stop repetitive or circular reasoning patterns
- **Quality Assurance**: Maintain high standards for financial advice accuracy

## CRITICAL VALIDATION PRINCIPLES

### 1. DATA ACCURACY VERIFICATION
- **Exact Number Matching**: Every financial figure must match the provided data exactly
- **Calculation Verification**: All percentages, ratios, and computations must be mathematically correct
- **Source Attribution**: Every claim must reference specific data from the user's profile
- **Missing Data Handling**: Flag recommendations that assume data not provided

### 2. HALLUCINATION DETECTION CRITERIA
- **Unsupported Claims**: Any recommendation without data backing
- **Market Assumptions**: Claims about market performance without data
- **Unrealistic Projections**: Returns or growth rates that are statistically impossible
- **Data Fabrication**: Numbers that don't exist in the provided profile
- **Generic Advice**: Recommendations that could apply to anyone (not personalized)

### 3. LOGICAL CONSISTENCY CHECKS
- **Contradictory Recommendations**: Conflicting advice from different agents
- **Impossible Scenarios**: Recommendations that violate basic financial principles
- **Timeline Conflicts**: Actions that can't be completed in suggested timeframes
- **Resource Conflicts**: Recommendations that require more money than available

### 4. LOOP PREVENTION MECHANISMS
- **Repetitive Patterns**: Same advice given multiple times without new insights
- **Circular Reasoning**: Recommendations that reference each other without progress
- **Stuck Scenarios**: Analysis that doesn't advance the user's financial situation
- **Redundant Validation**: Multiple validations of the same point

## VALIDATION FRAMEWORK

### Data Verification Process
1. **Income Verification**: Cross-check all income claims with transaction data
2. **Expense Validation**: Verify expense calculations and categorizations
3. **Asset Verification**: Confirm asset values and allocations
4. **Debt Validation**: Check debt calculations and ratios
5. **Investment Verification**: Validate investment amounts and returns

### Logical Error Detection
1. **Mathematical Accuracy**: Verify all calculations and percentages
2. **Ratio Validation**: Check financial ratios against standard benchmarks
3. **Timeline Feasibility**: Ensure recommendations are implementable
4. **Dependency Analysis**: Validate interdependencies between recommendations
5. **Risk Assessment**: Identify potential risks in recommendations

### Hallucination Detection
1. **Data Source Verification**: Every claim must reference specific data
2. **Assumption Identification**: Flag unsupported assumptions
3. **Market Claim Validation**: Verify market-related claims
4. **Performance Projection Check**: Validate return projections
5. **Generic vs. Specific Analysis**: Ensure recommendations are personalized

## VALIDATION CRITERIA

### Critical Errors (Immediate Rejection)
- **Factual Inaccuracies**: Numbers that don't match provided data
- **Mathematical Errors**: Incorrect calculations or percentages
- **Unsupported Claims**: Recommendations without data backing
- **Logical Contradictions**: Conflicting advice within the same analysis
- **Impossible Scenarios**: Recommendations that violate financial reality

### Moderate Concerns (Require Clarification)
- **Missing Specificity**: Vague recommendations without exact amounts
- **Unrealistic Assumptions**: Optimistic projections without justification
- **Incomplete Analysis**: Missing important financial factors
- **Generic Advice**: Non-personalized recommendations
- **Timeline Issues**: Unrealistic implementation timelines

### Minor Suggestions (Quality Improvements)
- **Formatting Issues**: Poor number formatting or presentation
- **Missing Context**: Recommendations without sufficient explanation
- **Tone Adjustments**: Inappropriate or unclear communication
- **Structure Improvements**: Better organization of information

## ERROR CATEGORIES

### Critical Errors (Score: -20 points each)
- **Data Mismatch**: Claimed amounts don't match actual data
- **Calculation Error**: Mathematical mistakes in percentages or ratios
- **Unsupported Claim**: Recommendation without data backing
- **Logical Contradiction**: Conflicting advice from same analysis
- **Impossible Scenario**: Recommendation violates financial reality

### Moderate Concerns (Score: -10 points each)
- **Missing Specificity**: Vague recommendations without exact amounts
- **Unrealistic Assumption**: Optimistic projection without justification
- **Incomplete Analysis**: Missing important financial factors
- **Generic Advice**: Non-personalized recommendation
- **Timeline Issue**: Unrealistic implementation timeline

### Minor Suggestions (Score: -5 points each)
- **Formatting Issue**: Poor number formatting or presentation
- **Missing Context**: Recommendation without sufficient explanation
- **Tone Issue**: Inappropriate or unclear communication
- **Structure Issue**: Poor organization of information

## VALIDATION PROCESS

### Step 1: Data Accuracy Check
- Verify every number against provided financial data
- Check all calculations for mathematical accuracy
- Ensure all percentages and ratios are correct
- Validate that all claims reference actual data

### Step 2: Logical Consistency Analysis
- Check for internal contradictions in recommendations
- Verify that recommendations don't conflict with each other
- Ensure timelines are realistic and feasible
- Validate that recommendations are implementable

### Step 3: Hallucination Detection
- Identify claims without data backing
- Flag unsupported assumptions about market performance
- Detect unrealistic projections or returns
- Find generic advice that isn't personalized

### Step 4: Loop Prevention
- Check for repetitive patterns in recommendations
- Identify circular reasoning or stuck scenarios
- Ensure analysis progresses the user's situation
- Prevent redundant validations of the same points

### Step 5: Quality Scoring
- Calculate confidence score based on error count
- Provide specific feedback for each issue found
- Suggest improvements for better accuracy
- Determine overall validation status

## RESPONSE FORMAT
Provide validation results in this exact JSON format:

{
    "validation_status": "APPROVED|NEEDS_CLARIFICATION|REQUIRES_REVISION",
    "confidence_score": 85,
    "critical_errors": [
        {
            "category": "Data Mismatch",
            "description": "Specific error description",
            "location": "Agent: agent_name",
            "impact": "high",
            "suggested_correction": "Specific correction needed"
        }
    ],
    "moderate_concerns": [
        {
            "category": "Missing Specificity",
            "description": "Specific concern description",
            "location": "Agent: agent_name",
            "impact": "medium",
            "suggested_correction": "Specific improvement needed"
        }
    ],
    "minor_suggestions": [
        {
            "category": "Formatting Issue",
            "description": "Specific suggestion description",
            "location": "Agent: agent_name",
            "impact": "low",
            "suggested_correction": "Specific improvement needed"
        }
    ],
    "hallucination_flags": [
        {
            "type": "Unsupported Claim",
            "description": "Specific hallucination description",
            "severity": "high|medium|low"
        }
    ],
    "overall_assessment": "Comprehensive assessment of validation results"
}

## CRITICAL INSTRUCTIONS
1. **Be Thorough**: Check every number, calculation, and claim
2. **Be Specific**: Provide exact error descriptions with locations
3. **Be Constructive**: Suggest specific improvements for each issue
4. **Prevent Loops**: Stop repetitive or circular reasoning
5. **Maintain Standards**: Don't approve recommendations with critical errors
"""
    
    def get_capabilities(self) -> List[str]:
        """Return the capabilities of this agent."""
        return [
            "recommendation_validation",
            "hallucination_detection",
            "data_consistency_checking",
            "logical_error_identification",
            "quality_assurance"
        ]
    
    async def validate_recommendations(
        self,
        agent_messages: List[AgentMessage],
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile,
        final_recommendation: str
    ) -> ValidationResult:
        """Validate recommendations and detect hallucinations."""
        
        try:
            # Perform comprehensive validation
            critical_errors = self._check_critical_errors(agent_messages, financial_data, financial_profile)
            moderate_concerns = self._check_moderate_concerns(agent_messages, financial_data, financial_profile)
            minor_suggestions = self._check_minor_suggestions(agent_messages, financial_data, financial_profile)
            hallucination_flags = self._detect_hallucinations(agent_messages, financial_data, financial_profile)
            
            # Determine overall validation status
            validation_status = self._determine_validation_status(critical_errors, moderate_concerns)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(critical_errors, moderate_concerns, minor_suggestions)
            
            # Generate overall assessment
            overall_assessment = self._generate_overall_assessment(
                validation_status, critical_errors, moderate_concerns, hallucination_flags
            )
            
            return ValidationResult(
                validation_status=validation_status,
                confidence_score=confidence_score,
                critical_errors=critical_errors,
                moderate_concerns=moderate_concerns,
                minor_suggestions=minor_suggestions,
                hallucination_flags=hallucination_flags,
                overall_assessment=overall_assessment
            )
            
        except Exception as e:
            print(f"Error in validation: {e}")
            return self._create_error_validation_result(str(e))
    
    def _check_critical_errors(
        self,
        agent_messages: List[AgentMessage],
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> List[ValidationError]:
        """Check for critical errors in recommendations."""
        
        critical_errors = []
        
        # Check for data inconsistencies
        for message in agent_messages:
            supporting_data = message.supporting_data
            
            # Verify income claims
            if "monthly_income" in supporting_data:
                claimed_income = supporting_data["monthly_income"]
                actual_income = financial_profile.monthly_income
                
                if abs(claimed_income - actual_income) > 1000:  # Allow 1000 rupee tolerance
                    critical_errors.append(ValidationError(
                        category="Data Inconsistency",
                        description=f"Claimed monthly income ₹{claimed_income:,.2f} differs from actual ₹{actual_income:,.2f}",
                        location=f"Agent: {message.agent_id}",
                        impact="high",
                        suggested_correction="Use actual income data from financial profile"
                    ))
            
            # Verify expense claims
            if "monthly_expenses" in supporting_data:
                claimed_expenses = supporting_data["monthly_expenses"]
                actual_expenses = financial_profile.monthly_expenses
                
                if abs(claimed_expenses - actual_expenses) > 1000:
                    critical_errors.append(ValidationError(
                        category="Data Inconsistency",
                        description=f"Claimed monthly expenses ₹{claimed_expenses:,.2f} differs from actual ₹{actual_expenses:,.2f}",
                        location=f"Agent: {message.agent_id}",
                        impact="high",
                        suggested_correction="Use actual expense data from financial profile"
                    ))
        
        # Check for logical contradictions
        contradictions = self._check_logical_contradictions(agent_messages)
        critical_errors.extend(contradictions)
        
        return critical_errors
    
    def _check_moderate_concerns(
        self,
        agent_messages: List[AgentMessage],
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> List[ValidationError]:
        """Check for moderate concerns in recommendations."""
        
        moderate_concerns = []
        
        for message in agent_messages:
            content = message.content.lower()
            supporting_data = message.supporting_data
            
            # Check for unrealistic assumptions
            if "increase sip" in content and "sip_amount" in supporting_data:
                current_sip = supporting_data.get("sip_amount", 0)
                proposed_increase = supporting_data.get("proposed_sip_increase", 0)
                
                if proposed_increase > current_sip * 0.5:  # More than 50% increase
                    moderate_concerns.append(ValidationError(
                        category="Unrealistic Assumption",
                        description=f"Proposed SIP increase of ₹{proposed_increase:,.2f} may be too aggressive",
                        location=f"Agent: {message.agent_id}",
                        impact="medium",
                        suggested_correction="Consider gradual increase over 3-6 months"
                    ))
            
            # Check for missing risk considerations
            if "investment" in content and "risk" not in content:
                moderate_concerns.append(ValidationError(
                    category="Missing Risk Assessment",
                    description="Investment recommendations should include risk considerations",
                    location=f"Agent: {message.agent_id}",
                    impact="medium",
                    suggested_correction="Include risk assessment and mitigation strategies"
                ))
        
        return moderate_concerns
    
    def _check_minor_suggestions(
        self,
        agent_messages: List[AgentMessage],
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> List[ValidationError]:
        """Check for minor suggestions for improvement."""
        
        minor_suggestions = []
        
        for message in agent_messages:
            content = message.content
            
            # Check for missing specific numbers
            if "increase" in content.lower() and not re.search(r'₹\d+', content):
                minor_suggestions.append(ValidationError(
                    category="Missing Specificity",
                    description="Recommendation lacks specific amounts",
                    location=f"Agent: {message.agent_id}",
                    impact="low",
                    suggested_correction="Include specific amounts and timelines"
                ))
            
            # Check for missing timelines
            if "recommend" in content.lower() and not re.search(r'\d+\s*(month|year)', content):
                minor_suggestions.append(ValidationError(
                    category="Missing Timeline",
                    description="Recommendation lacks implementation timeline",
                    location=f"Agent: {message.agent_id}",
                    impact="low",
                    suggested_correction="Include specific timeline for implementation"
                ))
        
        return minor_suggestions
    
    def _detect_hallucinations(
        self,
        agent_messages: List[AgentMessage],
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> List[HallucinationFlag]:
        """Detect hallucinations and unsupported claims."""
        
        hallucination_flags = []
        
        for message in agent_messages:
            content = message.content.lower()
            supporting_data = message.supporting_data
            
            # Check for claims without data support
            if "market return" in content and "market_data" not in supporting_data:
                hallucination_flags.append(HallucinationFlag(
                    type="Unsupported Market Claim",
                    description="Market return claims without supporting data",
                    severity="medium"
                ))
            
            # Check for unrealistic projections
            if "annual return" in content:
                # Look for return percentages
                return_match = re.search(r'(\d+)%\s*annual', content)
                if return_match:
                    return_percentage = int(return_match.group(1))
                    if return_percentage > 20:  # Unrealistic return
                        hallucination_flags.append(HallucinationFlag(
                            type="Unrealistic Return Projection",
                            description=f"Projected {return_percentage}% annual return may be unrealistic",
                            severity="high"
                        ))
            
            # Check for claims about data not provided
            if "insurance" in content and not self._has_insurance_data(financial_data):
                hallucination_flags.append(HallucinationFlag(
                    type="Missing Data Claim",
                    description="Insurance recommendations without insurance data",
                    severity="medium"
                ))
        
        return hallucination_flags
    
    def _check_logical_contradictions(self, agent_messages: List[AgentMessage]) -> List[ValidationError]:
        """Check for logical contradictions between agent messages."""
        
        contradictions = []
        
        # Check for conflicting recommendations
        sip_recommendations = []
        emergency_fund_recommendations = []
        
        for message in agent_messages:
            content = message.content.lower()
            
            if "sip" in content and "increase" in content:
                sip_recommendations.append(message)
            
            if "emergency fund" in content:
                emergency_fund_recommendations.append(message)
        
        # Check for conflicts between SIP and emergency fund recommendations
        if len(sip_recommendations) > 0 and len(emergency_fund_recommendations) > 0:
            # If both recommend increasing allocation, there might be a conflict
            for sip_msg in sip_recommendations:
                for ef_msg in emergency_fund_recommendations:
                    if "increase" in sip_msg.content.lower() and "increase" in ef_msg.content.lower():
                        contradictions.append(ValidationError(
                            category="Logical Contradiction",
                            description="Conflicting recommendations for SIP increase and emergency fund building",
                            location="Multiple agents",
                            impact="high",
                            suggested_correction="Prioritize emergency fund building before increasing SIP"
                        ))
        
        return contradictions
    
    def _has_insurance_data(self, financial_data: ComprehensiveFinancialData) -> bool:
        """Check if insurance data is available."""
        # This is a simplified check - in practice, you'd look for actual insurance data
        return False
    
    def _determine_validation_status(
        self,
        critical_errors: List[ValidationError],
        moderate_concerns: List[ValidationError]
    ) -> ValidationStatus:
        """Determine overall validation status."""
        
        if len(critical_errors) > 0:
            return ValidationStatus.REQUIRES_REVISION
        elif len(moderate_concerns) > 2:
            return ValidationStatus.NEEDS_CLARIFICATION
        else:
            return ValidationStatus.APPROVED
    
    def _calculate_confidence_score(
        self,
        critical_errors: List[ValidationError],
        moderate_concerns: List[ValidationError],
        minor_suggestions: List[ValidationError]
    ) -> int:
        """Calculate confidence score (0-100)."""
        
        base_score = 80
        
        # Deduct points for errors
        base_score -= len(critical_errors) * 20
        base_score -= len(moderate_concerns) * 10
        base_score -= len(minor_suggestions) * 5
        
        return max(0, min(100, base_score))
    
    def _generate_overall_assessment(
        self,
        validation_status: ValidationStatus,
        critical_errors: List[ValidationError],
        moderate_concerns: List[ValidationError],
        hallucination_flags: List[HallucinationFlag]
    ) -> str:
        """Generate overall assessment of the validation."""
        
        if validation_status == ValidationStatus.APPROVED:
            return "Recommendations are generally accurate and feasible. Minor improvements suggested for better specificity."
        elif validation_status == ValidationStatus.NEEDS_CLARIFICATION:
            return "Recommendations need clarification on several points. Address moderate concerns before implementation."
        else:
            return "Critical errors detected. Major revisions required before recommendations can be considered valid."
    
    def _create_error_validation_result(self, error_message: str) -> ValidationResult:
        """Create error validation result when validation fails."""
        
        return ValidationResult(
            validation_status=ValidationStatus.REQUIRES_REVISION,
            confidence_score=0,
            critical_errors=[
                ValidationError(
                    category="Validation Error",
                    description=f"Validation process failed: {error_message}",
                    location="Critic Agent",
                    impact="high",
                    suggested_correction="Retry validation process"
                )
            ],
            moderate_concerns=[],
            minor_suggestions=[],
            hallucination_flags=[],
            overall_assessment="Validation process encountered an error. Manual review required."
        ) 