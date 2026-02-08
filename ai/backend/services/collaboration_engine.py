import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.data_agent import DataAgent
from agents.cash_flow_agent import CashFlowAgent
from agents.investment_agent import InvestmentAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.critic_agent import CriticAgent
from models.agent_messages import Agent, CollaborativeSession, ValidationResult, AgentMessage, ConfidenceLevel
from models.financial_data import ComprehensiveFinancialData, FinancialProfile


class CollaborationEngine:
    """Main engine for orchestrating multi-agent financial analysis."""
    
    def __init__(self):
        """Initialize the collaboration engine with all agents."""
        self.data_agent = DataAgent()
        self.cash_flow_agent = CashFlowAgent()
        self.investment_agent = InvestmentAgent()
        self.coordinator_agent = CoordinatorAgent()
        self.critic_agent = CriticAgent()
        
        # Define participating agents
        from models.agent_messages import AgentCapability
        
        self.participating_agents = [
            Agent(
                id="data_agent",
                name="Data Agent",
                description="Financial data aggregation and processing",
                capabilities=[AgentCapability.DATA_AGGREGATION, AgentCapability.PROFILE_COMPILATION],
                specialties=["Data processing", "Profile compilation"],
                color="#4CAF50"
            ),
            Agent(
                id="cash_flow_agent",
                name="Cash Flow Agent",
                description="Income, expenses, and cash flow analysis",
                capabilities=[AgentCapability.CASH_FLOW_ANALYSIS, AgentCapability.BUDGET_OPTIMIZATION],
                specialties=["Income analysis", "Expense optimization"],
                color="#2196F3"
            ),
            Agent(
                id="investment_agent",
                name="Investment Agent",
                description="Portfolio analysis and investment strategies",
                capabilities=[AgentCapability.INVESTMENT_ANALYSIS, AgentCapability.PORTFOLIO_OPTIMIZATION],
                specialties=["Portfolio analysis", "Investment strategies"],
                color="#FF9800"
            ),
            Agent(
                id="coordinator_agent",
                name="Coordinator Agent",
                description="Multi-agent orchestration and consensus building",
                capabilities=[AgentCapability.COORDINATION, AgentCapability.CONSENSUS_BUILDING],
                specialties=["Orchestration", "Consensus building"],
                color="#9C27B0"
            ),
            Agent(
                id="critic_agent",
                name="Critic Agent",
                description="Validation and quality assurance",
                capabilities=[AgentCapability.VALIDATION, AgentCapability.QUALITY_ASSURANCE],
                specialties=["Validation", "Hallucination detection"],
                color="#F44336"
            )
        ]
    
    async def process_user_query(
        self,
        user_query: str,
        phone_number: str
    ) -> Dict[str, Any]:
        """Process user query through the multi-agent collaboration system."""
        
        try:
            print(f"🚀 Starting multi-agent analysis for query: {user_query}")
            
            # Step 1: Data Aggregation with Validation
            print("📊 Step 1: Aggregating and validating financial data...")
            financial_data = await self.data_agent.compile_financial_profile(phone_number)
            financial_profile = await self.data_agent.process_financial_profile(financial_data)
            
            # Validate data completeness
            data_validation = self._validate_financial_data(financial_data, financial_profile)
            if not data_validation["is_valid"]:
                print(f"⚠️ Data validation issues: {data_validation['issues']}")
            
            print(f"✅ Financial data compiled: Net worth ₹{financial_data.net_worth.totalNetWorth:,.2f}")
            
            # Step 2: Multi-Agent Collaboration with Loop Prevention
            print("🤖 Step 2: Orchestrating multi-agent collaboration...")
            session = await self.coordinator_agent.orchestrate_collaboration(
                user_query=user_query,
                financial_data=financial_data,
                financial_profile=financial_profile,
                participating_agents=self.participating_agents
            )
            
            # Check for collaboration loops
            loop_detection = self._detect_collaboration_loops(session)
            if loop_detection["has_loop"]:
                print(f"⚠️ Collaboration loop detected: {loop_detection['description']}")
                session = await self._resolve_collaboration_loop(session, loop_detection)
            
            print(f"✅ Collaboration completed: {len(session.agent_messages)} agent messages")
            
            # Step 3: Enhanced Validation with Hallucination Detection
            print("🔍 Step 3: Validating recommendations and detecting hallucinations...")
            validation_result = await self.critic_agent.validate_recommendations(
                agent_messages=session.agent_messages,
                financial_data=financial_data,
                financial_profile=financial_profile,
                final_recommendation=session.final_recommendation
            )
            
            # Check for critical validation issues
            if validation_result.validation_status.value == "REQUIRES_REVISION":
                print(f"⚠️ Critical validation issues found: {len(validation_result.critical_errors)} errors")
                session = await self._handle_validation_failure(session, validation_result)
            
            print(f"✅ Validation completed: Confidence score {validation_result.confidence_score}")
            
            # Step 4: Prepare Enhanced Response
            print("📝 Step 4: Preparing comprehensive response...")
            response = self._prepare_enhanced_response(
                session=session,
                validation_result=validation_result,
                financial_profile=financial_profile,
                data_validation=data_validation
            )
            
            print("✅ Multi-agent analysis completed successfully")
            return response
            
        except Exception as e:
            print(f"❌ Error in multi-agent analysis: {e}")
            return self._create_error_response(str(e))
    
    def _validate_financial_data(
        self,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> Dict[str, Any]:
        """Validate financial data completeness and quality."""
        
        issues = []
        is_valid = True
        
        # Check for missing critical data
        if not financial_data.net_worth or financial_data.net_worth.totalNetWorth == 0:
            issues.append("Missing or zero net worth data")
            is_valid = False
        
        # Note: Income/expense data may not be available from MCP service
        # Only validate if the data exists
        if hasattr(financial_profile, 'monthly_income') and financial_profile.monthly_income:
            if hasattr(financial_profile, 'monthly_expenses') and financial_profile.monthly_expenses:
                if financial_profile.monthly_expenses > financial_profile.monthly_income:
                    issues.append("Monthly expenses exceed monthly income")
                    is_valid = False
        
        # Check for reasonable data ranges
        if financial_profile.monthly_income > 1000000:  # ₹10 lakhs
            issues.append("Unusually high monthly income - data may be incorrect")
        
        if financial_profile.total_debt > 10000000:  # ₹1 crore
            issues.append("Unusually high debt - data may be incorrect")
        
        return {
            "is_valid": is_valid,
            "issues": issues,
            "data_quality_score": self._calculate_data_quality_score(financial_data, financial_profile)
        }
    
    def _calculate_data_quality_score(
        self,
        financial_data: ComprehensiveFinancialData,
        financial_profile: FinancialProfile
    ) -> float:
        """Calculate data quality score (0-100)."""
        
        score = 100
        total_checks = 0
        
        # Check data completeness
        checks = [
            (financial_data.net_worth is not None, 15),
            (financial_data.bank_transactions, 15),
            (financial_data.credit_report, 15),
            (financial_data.mf_transactions, 15),
            (financial_data.epf_details, 15),
            (financial_profile.total_assets > 0, 10),
            (financial_profile.total_debt >= 0, 10),
            (financial_profile.credit_score > 0, 5)
        ]
        
        for check, points in checks:
            total_checks += points
            if not check:
                score -= points
        
        return max(0, score)
    
    def _detect_collaboration_loops(self, session: CollaborativeSession) -> Dict[str, Any]:
        """Detect collaboration loops and repetitive patterns."""
        
        has_loop = False
        description = ""
        
        # Check for repetitive agent messages
        agent_message_counts = {}
        for message in session.agent_messages:
            agent_id = message.agent_id
            agent_message_counts[agent_id] = agent_message_counts.get(agent_id, 0) + 1
        
        # Check for excessive messages from same agent
        for agent_id, count in agent_message_counts.items():
            if count > 3:  # More than 3 messages from same agent
                has_loop = True
                description = f"Excessive messages from {agent_id}: {count} messages"
                break
        
        # Check for circular dependencies
        dependencies = []
        for message in session.agent_messages:
            if hasattr(message, 'dependencies'):
                dependencies.extend(message.dependencies)
        
        if len(set(dependencies)) < len(dependencies):
            has_loop = True
            description = "Circular dependencies detected between agents"
        
        # Check for stuck iterations
        if session.current_iteration > 5:
            has_loop = True
            description = f"Too many iterations: {session.current_iteration}"
        
        return {
            "has_loop": has_loop,
            "description": description,
            "agent_message_counts": agent_message_counts,
            "iteration_count": session.current_iteration
        }
    
    async def _resolve_collaboration_loop(
        self,
        session: CollaborativeSession,
        loop_detection: Dict[str, Any]
    ) -> CollaborativeSession:
        """Resolve collaboration loops by forcing consensus."""
        
        print(f"🔄 Resolving collaboration loop: {loop_detection['description']}")
        
        # Force final recommendation based on available data
        if session.agent_messages:
            # Use the most recent high-confidence message
            best_message = max(
                session.agent_messages,
                key=lambda m: getattr(m, 'confidence_level', ConfidenceLevel.LOW).value
            )
            
            session.final_recommendation = f"""
I've analyzed your financial situation and here's my recommendation:

{best_message.content}

Based on the available data, this is the most reliable advice I can provide. 
For more detailed analysis, please ensure all your financial data is up to date.
"""
        
        session.current_iteration = 6  # Mark as resolved
        return session
    
    async def _handle_validation_failure(
        self,
        session: CollaborativeSession,
        validation_result: ValidationResult
    ) -> CollaborativeSession:
        """Handle validation failures by creating a safe response."""
        
        print(f"⚠️ Handling validation failure with {len(validation_result.critical_errors)} critical errors")
        
        # Create a safe, conservative response
        safe_recommendation = f"""
I've reviewed your financial situation, but I need to be cautious with my recommendations due to some data inconsistencies.

Your current situation:
- Net worth: ₹{getattr(session.context.get('financial_data', {}), 'net_worth', {}).get('totalNetWorth', 0):,.2f}
- Monthly income: ₹{getattr(session.context.get('financial_profile', {}), 'monthly_income', 0):,.2f}

General recommendations:
- Review your financial data for accuracy
- Focus on building an emergency fund
- Consider consulting with a financial advisor
- Track your expenses regularly

For more specific advice, please ensure all your financial information is accurate and up to date.
"""
        
        session.final_recommendation = safe_recommendation
        return session
    
    def _prepare_enhanced_response(
        self,
        session: CollaborativeSession,
        validation_result: ValidationResult,
        financial_profile: FinancialProfile,
        data_validation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare enhanced response with comprehensive information."""
        
        # Extract key statistics from agent messages
        statistics = self._extract_statistics_from_messages(session.agent_messages)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            validation_result.confidence_score,
            data_validation["data_quality_score"]
        )
        
        return {
            "success": True,
            "response": session.final_recommendation,
            "metadata": {
                "session_id": session.session_id,
                "iteration_count": session.current_iteration,
                "agent_count": len(session.agent_messages),
                "validation_status": validation_result.validation_status.value,
                "confidence_score": overall_confidence,
                "data_quality_score": data_validation["data_quality_score"],
                "processing_timestamp": datetime.utcnow().isoformat()
            },
            "validation": {
                "status": validation_result.validation_status.value,
                "confidence_score": validation_result.confidence_score,
                "critical_errors": len(validation_result.critical_errors),
                "moderate_concerns": len(validation_result.moderate_concerns),
                "minor_suggestions": len(validation_result.minor_suggestions),
                "hallucination_flags": len(validation_result.hallucination_flags),
                "overall_assessment": validation_result.overall_assessment
            },
            "statistics": statistics,
            "agent_insights": self._extract_agent_insights(session.agent_messages),
            "recommendations": self._extract_recommendations(session.agent_messages),
            "risks_and_opportunities": self._extract_risks_and_opportunities(session.agent_messages)
        }
    
    def _extract_statistics_from_messages(self, agent_messages: List[AgentMessage]) -> Dict[str, Any]:
        """Extract key statistics from agent messages."""
        
        statistics = {
            "financial_metrics": {},
            "performance_indicators": {},
            "risk_metrics": {}
        }
        
        for message in agent_messages:
            if hasattr(message, 'supporting_data') and message.supporting_data:
                # Extract calculations and statistics
                if 'calculations' in message.supporting_data:
                    statistics["financial_metrics"].update(message.supporting_data['calculations'])
                
                if 'statistics' in message.supporting_data:
                    statistics["performance_indicators"].update(message.supporting_data['statistics'])
        
        return statistics
    
    def _calculate_overall_confidence(
        self,
        validation_confidence: int,
        data_quality_score: float
    ) -> float:
        """Calculate overall confidence score."""
        
        # Weight validation confidence more heavily
        weighted_confidence = (validation_confidence * 0.7) + (data_quality_score * 0.3)
        return min(100, max(0, weighted_confidence))
    
    def _extract_agent_insights(self, agent_messages: List[AgentMessage]) -> List[Dict[str, Any]]:
        """Extract insights from agent messages."""
        
        insights = []
        for message in agent_messages:
            if message.message_type.value == "ANALYSIS":
                insights.append({
                    "agent": message.agent_id,
                    "insight": message.content,
                    "confidence": message.confidence_level.value,
                    "timestamp": message.timestamp.isoformat()
                })
        
        return insights
    
    def _extract_recommendations(self, agent_messages: List[AgentMessage]) -> List[Dict[str, Any]]:
        """Extract recommendations from agent messages."""
        
        recommendations = []
        for message in agent_messages:
            if hasattr(message, 'supporting_data') and message.supporting_data:
                if 'recommendations' in message.supporting_data:
                    for rec in message.supporting_data['recommendations']:
                        recommendations.append({
                            "agent": message.agent_id,
                            "recommendation": rec,
                            "confidence": message.confidence_level.value
                        })
        
        return recommendations
    
    def _extract_risks_and_opportunities(self, agent_messages: List[AgentMessage]) -> Dict[str, List[str]]:
        """Extract risks and opportunities from agent messages."""
        
        risks = []
        opportunities = []
        
        for message in agent_messages:
            if hasattr(message, 'supporting_data') and message.supporting_data:
                if 'risks' in message.supporting_data:
                    risks.extend(message.supporting_data['risks'])
                
                if 'opportunities' in message.supporting_data:
                    opportunities.extend(message.supporting_data['opportunities'])
        
        return {
            "risks": list(set(risks)),  # Remove duplicates
            "opportunities": list(set(opportunities))
        }
    
    def _prepare_response(
        self,
        session: CollaborativeSession,
        validation_result: ValidationResult,
        financial_profile: FinancialProfile
    ) -> Dict[str, Any]:
        """Prepare the final response for the user."""
        
        # Determine response quality based on validation
        if validation_result.validation_status.value == "APPROVED":
            response_quality = "high"
            confidence_message = "High confidence in recommendations"
        elif validation_result.validation_status.value == "NEEDS_CLARIFICATION":
            response_quality = "medium"
            confidence_message = "Moderate confidence - some clarifications needed"
        else:
            response_quality = "low"
            confidence_message = "Low confidence - major revisions required"
        
        # Prepare agent insights
        agent_insights = []
        for message in session.agent_messages:
            if message.message_type.value == "analysis":
                agent_insights.append({
                    "agent": message.agent_id,
                    "insight": message.content,
                    "confidence": message.confidence_level.value,
                    "supporting_data": message.supporting_data
                })
        
        # Prepare validation summary
        validation_summary = {
            "status": validation_result.validation_status.value,
            "confidence_score": validation_result.confidence_score,
            "critical_errors": len(validation_result.critical_errors),
            "moderate_concerns": len(validation_result.moderate_concerns),
            "minor_suggestions": len(validation_result.minor_suggestions),
            "hallucination_flags": len(validation_result.hallucination_flags),
            "overall_assessment": validation_result.overall_assessment
        }
        
        # Create comprehensive response
        response = {
            "success": True,
            "query": session.user_query,
            "session_id": session.session_id,
            "response_quality": response_quality,
            "confidence_message": confidence_message,
            "final_recommendation": session.final_recommendation,
            "agent_insights": agent_insights,
            "validation_summary": validation_summary,
            "financial_profile": {
                "monthly_income": financial_profile.monthly_income,
                "monthly_expenses": financial_profile.monthly_expenses,
                "discretionary_income": financial_profile.discretionary_income,
                "total_assets": financial_profile.total_assets,
                "total_debt": financial_profile.total_debt,
                "credit_score": financial_profile.credit_score,
                "portfolio_value": financial_profile.portfolio_value,
                "financial_stability_score": financial_profile.financial_stability_score
            },
            "collaboration_metadata": {
                "participating_agents": len(session.participating_agents),
                "total_messages": len(session.agent_messages),
                "phases_completed": session.current_iteration,
                "max_iterations": session.max_iterations,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        return response
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response when processing fails."""
        
        return {
            "success": False,
            "error": error_message,
            "response_quality": "error",
            "confidence_message": "Unable to process request due to technical error",
            "final_recommendation": "Please try again or contact support if the issue persists.",
            "agent_insights": [],
            "validation_summary": {
                "status": "ERROR",
                "confidence_score": 0,
                "critical_errors": 1,
                "moderate_concerns": 0,
                "minor_suggestions": 0,
                "hallucination_flags": 0,
                "overall_assessment": "Processing failed due to technical error"
            },
            "financial_profile": {},
            "collaboration_metadata": {
                "participating_agents": 0,
                "total_messages": 0,
                "phases_completed": 0,
                "max_iterations": 0,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents in the system."""
        
        agents_status = {}
        
        for agent in self.participating_agents:
            # Check if agent is available (simplified check)
            try:
                # This would involve more sophisticated health checks
                agents_status[agent.id] = {
                    "name": agent.name,
                    "status": "available",
                    "capabilities": agent.capabilities,
                    "specialties": agent.specialties,
                    "color": agent.color
                }
            except Exception as e:
                agents_status[agent.id] = {
                    "name": agent.name,
                    "status": "error",
                    "error": str(e),
                    "capabilities": agent.capabilities,
                    "specialties": agent.specialties,
                    "color": agent.color
                }
        
        return {
            "total_agents": len(self.participating_agents),
            "available_agents": len([a for a in agents_status.values() if a["status"] == "available"]),
            "agents": agents_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_collaboration_history(self, session_id: str) -> Optional[CollaborativeSession]:
        """Get collaboration history for a specific session."""
        
        # This would typically involve database lookup
        # For now, return None as sessions are not persisted
        return None
    
    def _log_collaboration_event(self, event_type: str, details: Dict[str, Any]):
        """Log collaboration events for monitoring and debugging."""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        # In a production system, this would be logged to a proper logging system
        print(f"📝 Collaboration Event: {event_type} - {details}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the collaboration engine."""
        
        health_status = {
            "engine_status": "healthy",
            "agents_status": {},
            "data_sources_status": "unknown",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Check each agent
        for agent in self.participating_agents:
            try:
                # Simple availability check
                health_status["agents_status"][agent.id] = "healthy"
            except Exception as e:
                health_status["agents_status"][agent.id] = f"error: {str(e)}"
                health_status["engine_status"] = "degraded"
        
        return health_status 