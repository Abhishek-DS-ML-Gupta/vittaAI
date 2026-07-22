"""
VittaAI - Investment Advisor Module
Provides personalized investment recommendations and portfolio guidance
"""

import re
import random
from typing import Dict, Any, Optional
from financial_assistant import FinancialAssistant


class InvestmentAdvisor:
    def __init__(self, client, localization_manager, 
                 available_stocks: Optional[list] = None):
        """
        Initialize Investment Advisor
        
        Args:
            client: Groq API client
            localization_manager: Localization manager for translations
            available_stocks: Default list of popular stocks
        """
        self.client = client
        self.localization = localization_manager
        self.available_stocks = available_stocks or ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 
                                                     'NVDA', 'META', 'JPM', 'V', 'WMT']
        
        # Investment knowledge base
        self.investment_guidelines = {
            'conservative': {"risk_tolerance": "low", "expected_return": "3-6%", "suggested_allocation": "60% bonds, 30% stocks, 10% cash"},
            'moderate': {"risk_tolerance": "medium", "expected_return": "6-10%", "suggested_allocation": "40% stocks, 50% bonds, 10% cash"},
            'aggressive': {"risk_tolerance": "high", "expected_return": "10-15%", "suggested_allocation": "70% stocks, 25% bonds, 5% cash"}
        }

    def get_investment_recommendation(self, query: str, language: str = "en") -> Dict[str, Any]:
        """
        Generate investment recommendation based on user query
        
        Args:
            query: User's investment-related query
            language: Language for response
            
        Returns:
            Response dictionary with recommendation and analysis
        """
        response = {
            'response': "",
            'type': "investment_recommendation",
            'confidence': 0.0,
            'suggestions': [],
            'risk_free': False
        }

        # Analyze user's risk tolerance
        risk_level = self._analyze_risk_tolerance(query)
        guidelines = self.investment_guidelines.get(risk_level, self.investment_guidelines['moderate'])
        
        # Analyze investment preferences
        preferences = self._analyze_investment_preferences(query)
        
        # Generate personalized recommendation
        personal_response = self._generate_investment_advice(query, risk_level, guidelines, preferences, language)
        
        response['response'] = personal_response
        response['confidence'] = 0.85 if risk_level != 'unknown' else 0.65
        response['suggestions'] = self._generate_suggestions(risk_level, preferences)
        
        if risk_level == 'unknown':
            response['risk_free'] = True

        return response

    def _analyze_risk_tolerance(self, query: str) -> str:
        """Determine user's risk tolerance based on query"""
        query_lower = query.lower()
        
        # Conservative keywords
        conservative_keywords = ['safe', 'conservative', 'low risk', 'certain', 'steady']
        if any(keyword in query_lower for keyword in conservative_keywords):
            return 'conservative'
        
        # Aggressive keywords
        aggressive_keywords = ['aggressive', 'high risk', 'maximum', 'high return', 'growth', 'dramatic']
        if any(keyword in query_lower for keyword in aggressive_keywords):
            return 'aggressive'
        
        # Moderate keywords
        moderate_keywords = ['balanced', 'moderate', 'reasonable', 'balanced portfolio', 'middle ground']
        if any(keyword in query_lower for keyword in moderate_keywords):
            return 'moderate'
        
        return 'moderate'  # Default to moderate

    def _analyze_investment_preferences(self, query: str) -> Dict[str, Any]:
        """Analyze user's investment preferences"""
        preferences = {
            'sector': 'unknown',
            'investment_size': 'unknown',
            'time_horizon': 'medium'
        }
        
        query_lower = query.lower()
        
        # Sector preferences
        tech_keywords = ['tech', 'technology', 'software', 'ai', 'computers', 'software']
        finance_keywords = ['finance', 'financial', 'bank', 'investment', 'brokerage']
        healthcare_keywords = ['healthcare', 'medical', 'pharmaceutical', 'covid']
        energy_keywords = ['energy', 'oil', 'petroleum', 'gas', 'renewable', 'solar', 'wind']
        consumer_keywords = ['consumer', 'retail', 'shopping', 'social media', 'streaming']
        
        if any(keyword in query_lower for keyword in tech_keywords):
            preferences['sector'] = 'technology'
        elif any(keyword in query_lower for keyword in finance_keywords):
            preferences['sector'] = 'finance'
        elif any(keyword in query_lower for keyword in healthcare_keywords):
            preferences['sector'] = 'healthcare'
        elif any(keyword in query_lower for keyword in energy_keywords):
            preferences['sector'] = 'energy'
        elif any(keyword in query_lower for keyword in consumer_keywords):
            preferences['sector'] = 'consumer'

        # Investment size
        large_keywords = ['large portfolio', 'wealthy', 'high net worth', 'expensive', 'major']
        small_keywords = ['small', 'beginner', 'limited', 'conservative', 'safe']
        if any(keyword in query_lower for keyword in large_keywords):
            preferences['investment_size'] = 'large'
        elif any(keyword in query_lower for keyword in small_keywords):
            preferences['investment_size'] = 'small'

        # Time horizon
        short_keywords = ['short', 'quick', 'immediate', 'months', 'quick return']
        long_keywords = ['long term', 'years', 'decades', 'retirement', 'permanent']
        if any(keyword in query_lower for keyword in short_keywords):
            preferences['time_horizon'] = 'short'
        elif any(keyword in query_lower for keyword in long_keywords):
            preferences['time_horizon'] = 'long'
        
        return preferences

    def _generate_investment_advice(self, query: str, risk_level: str, 
                                  guidelines: Dict, preferences: Dict, 
                                  language: str) -> str:
        """Generate personalized investment advice"""
        
        # Analysis prompt using Groq API
        analysis_prompt = f"""You are VittaAI's expert Investment Advisor. Analyse this user query: "{query}".

        User Risk Tolerance: {risk_level}
        Investment Guidelines: {guidelines}
        User Preferences: {preferences}

        Provide investment advice in {language} focusing on:
        1. Current market context and conditions (generally, don't specify recent dates)
        2. Recommended investment approach based on risk tolerance and preferences
        3. Specific asset classes or sectors suggested
        4. Suggested portfolio allocation (percentage breakdown)
        5. Expected outcomes with realistic timeframes
        6. Important considerations and potential risks
        7. Specific actionable recommendations

        Format your response clearly, starting with a brief summary, then detailed analysis."""

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are VittaAI's expert Investment Advisor. Provide detailed, accurate, and personalized investment recommendations. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return completion.choices[0].message.content or "Unable to generate investment advice based on current market conditions."
            
        except Exception as e:
            # Fallback to structured response if API fails
            return self._generate_fallback_investment_advice(risk_level, guidelines, preferences, language)

    def _generate_fallback_investment_advice(self, risk_level: str, 
                                           guidelines: Dict, 
                                           preferences: Dict, 
                                           language: str) -> str:
        """Generate structured fallback investment advice"""
        
        # Get relevant suggestions
        recommendations = self._get_sector_recommendations(preferences['sector'])
        portfolio_suggestions = guidelines['suggested_allocation']
        expected_return = guidelines['expected_return']
        
        fallback_response = f"""# Investment Analysis for {risk_level.capitalize()} Profile

## Risk Guide
- Risk Tolerance: {guidelines['risk_tolerance']} 
- Expected Return: {expected_return}

## Portfolio Recommendations
Based on your preferences:

**{portfolio_suggestions}**

## Sector-Specific Suggestions
{recommendations}

## Investment Considerations
1. Diversification is key to managing risk
2. Consider both short-term opportunities and long-term growth
3. Review market conditions regularly
4. Adjust your portfolio as your financial goals evolve

## Risk Warning
Investments always carry risk. Past performance does not guarantee future results. Consider consulting a professional financial advisor for personalized advice.

## Time Horizons
- Short-term: <2 years (lower risk tolerance)
- Medium-term: 2-5 years
- Long-term: 5+ years (higher growth potential)

VittaAI provides this information for educational purposes only."""
        
        return fallback_response

    def _get_sector_recommendations(self, sector: str) -> str:
        """Get sector-specific investment recommendations"""
        recommendations = {
            'technology': """
        **Technology Sector Opportunities**
        - Large-cap tech (AAPL, MSFT, GOOGL) for stability
        - Emerging AI and semiconductor companies for growth
        - Consider defensive tech stocks for portfolio defense
        - Watch for regulatory developments and innovation trends""",
            'finance': """
        **Finance Sector Opportunities**
        - Major banks (JPM, V) for steady dividends
        - Insurers for stability and consistent returns
        - Financial technology (FinTech) for growth potential
        - Watch for interest rate environments""",
            'healthcare': """
        **Healthcare Sector Opportunities**
        - Pharmaceuticals for reliable earnings
        - Healthcare services for stability
        - Medical technology for innovation opportunities
        - Consider defensive nature for portfolio balance""",
            'energy': """
        **Energy Sector Opportunities**
        - Renewable energy for long-term growth
        - Traditional energy for stability
        - Energy storage solutions for emerging opportunities
        - Watch for policy and regulatory changes""",
            'consumer': """
        **Consumer Sector Opportunities**
        - E-commerce leaders for growth
        - Traditional retail for stable dividends
        - Consumer discretionary for economic resilience
        - Consider discretionary vs staples balance"""
        }
        
        return recommendations.get(sector, """
        **General Sector Diversification**
        - Consider a blend of Large-cap, Mid-cap, and Small-cap stocks
        - Mix of established companies for stability and emerging companies for growth
        - Balance across different economic cycles""")

    def _generate_suggestions(self, risk_level: str, preferences: Dict) -> list:
        """Generate actionable suggestions based on profile"""
        suggestions = []
        
        if risk_level == 'conservative':
            suggestions.extend([
                "Start with a core-satellite strategy: core for stability, satellites for growth",
                "Consider fixed-income investments for consistent returns",
                "Focus on companies with strong balance sheets and consistent dividends",
                "Diversify internationally to reduce specific market risks"
            ])
        elif risk_level == 'aggressive':
            suggestions.extend([
                "Consider sector rotation to capture changing market trends",
                "Research and invest in high-growth emerging companies",
                "Use dollar-cost averaging to reduce market timing risk",
                "Diversify across different time horizons and asset classes"
            ])
        
        # Sector-specific suggestions
        if preferences['sector'] != 'unknown':
            suggestions.append(f"Focus on {preferences['sector'].capitalize()} sector opportunities")
        
        if preferences['investment_size'] == 'small':
            suggestions.extend([
                "Start with index funds or ETFs for broad diversification",
                "Consider fractional shares for high-priced investments",
                "Build core investments gradually through regular contributions"
            ])
        
        if preferences['time_horizon'] == 'short':
            suggestions.extend([
                "Focus on liquid assets for easy access",
                "Consider short-term bond ETFs for capital preservation",
                "Avoid allocations to illiquid investments"
            ])
        
        # General best practices
        suggestions.extend([
            "Regular portfolio reviews every 6 months",
            "Dollar-cost average into your positions",
            "Consider tax-efficient investment vehicles"
        ])
        
        return suggestions[:5]  # Return top 5 suggestions

    def analyze_portfolio(self, portfolio_str: str, language: str = "en") -> Dict[str, Any]:
        """
        Analyze a given portfolio string and provide evaluation
        
        Args:
            portfolio_str: String representation of portfolio (e.g., "AAPL 20, GOOGL 30, TSLA 50")
            language: Language for response
            
        Returns:
            Analysis with strengths, weaknesses, and recommendations
        """
        analysis = {
            'response': "",
            'type': "portfolio_analysis",
            'confidence': 0.0,
            'suggestions': []
        }
        
        # Parse portfolio
        portfolio = self._parse_portfolio(portfolio_str)
        
        if portfolio:
            analysis_response = self._generate_portfolio_analysis(portfolio, language)
            analysis['response'] = analysis_response
            analysis['confidence'] = 0.80
            analysis['suggestions'] = self._generate_portfolio_suggestions(portfolio)
        else:
            analysis['response'] = "Unable to parse portfolio. Please use format like 'AAPL 20, GOOGL 30, TSLA 50'"
            
        return analysis

    def _parse_portfolio(self, portfolio_str: str) -> Dict[str, float]:
        """Parse portfolio string into symbol to allocation mapping"""
        portfolio = {}
        try:
            # Split by comma and process each entry
            entries = portfolio_str.split(',')
            for entry in entries:
                entry = entry.strip()
                if not entry:
                    continue
                # Try to find symbol and percentage (supports multiple formats)
                parts = re.findall(r'([A-Z]+)\s*[:\.\-]?|(\d+(?:\.\d+)?)$', entry)
                if len(parts) >= 2:
                    symbol = (parts[0][0] if parts[0] else '').upper()
                    percentage = float(parts[1][0]) if parts[1] else 0.0
                    if symbol and 0 < percentage <= 100:
                        portfolio[symbol] = percentage
        except Exception as e:
            print(f"Error parsing portfolio: {e}")
        
        return portfolio

    def _generate_portfolio_analysis(self, portfolio: Dict[str, float], language: str) -> str:
        """Generate portfolio analysis using Groq API"""
        
        analysis_prompt = f"""You are an expert investment advisor analysing this portfolio:

        Portfolio:
        {json.dumps(portfolio, indent=2)}

        Provide a comprehensive analysis including:
        1. Overall portfolio balance and risk assessment
        2. Diversification quality (number of holdings, sector distribution)
        3. Performance considerations for each position
        4. Sector concentration and risks
        5. Valuation considerations
        6. Recommendations for improvement
        7. Risk warnings and considerations

        Format with clear headings, numbered list for recommendations, and include specific suggestions where applicable."""

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert investment advisor providing detailed portfolio analysis and actionable recommendations."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return completion.choices[0].message.content or "Unable to complete portfolio analysis."
            
        except Exception as e:
            # Fallback to constrained analysis
            return self._generate_portfolio_fallback_analysis(portfolio)

    def _generate_portfolio_fallback_analysis(self, portfolio: Dict[str, float]) -> str:
        """Generate basic portfolio analysis fallback"""
        holdings = len(portfolio)
        symbols = ', '.join(portfolio.keys())
        
        fallback_response = f"""# Portfolio Analysis - {holdings} Holdings

## Portfolio Overview
**Held Sectors:** {symbols}
**Total Positions:** {holdings}

## Current Assessment
**Diversification Status:**
- Single-sector concentration: {self._check_sector_concentration(portfolio) == 'High' if holdings <= 2 else 'Low' if holdings >= 5 else 'Medium'}
- Position count: {holdings} (Ideally 10-20 for proper diversification)

## Sector Contribution (Estimated)
Based on sector trends, if you have these popular sectors:

**Assumed Sector Breakdown:**
- Technology: {round(self._get_sector_percentage(portfolio, ['TECH', 'TECHNOLOGY', 'ZEUS', 'ZEUS'], '') or 0, 1)}%
- Healthcare: {round(self._get_sector_percentage(portfolio, ['HEALTH', 'H', 'AMZN'], '') or 0, 1)}%
- Consumer: {round(self._get_sector_percentage(portfolio, ['FIN', 'FINANCE', FINANCIAL], '') or 0, 1)}%
- Undiversified: %)

## Recommendations
1. **Consider Additional Diversification**: Introduce holdings from underrepresented sectors
2. **Optimal Position Count**: Aim for 10-15 holdings for balanced diversification
3. **Sector Rotation Opportunities**: Monitor sector performance and rotate as markets shift

## Risk Considerations
- Sector concentration provides both growth and concentrated risk
- Single-sector risks are higher than broad-market approaches
- Consider adding bonds or cash equivalents

## Next Steps
1. Review each position's fundamentals and performance
2. Consider rebalancing if allocation drift exceeds 5%
3. Regular portfolio monitoring recommended
4. Consider professional advice for complex portfolios

VittaAI provides this for educational purposes. Always consider seeking professional financial advice for significant investments."""
        
        return fallback_response

    def _generate_portfolio_suggestions(self, portfolio: Dict[str, float]) -> list:
        """Generate portfolio-specific suggestions"""
        suggestions = []
        
        if len(portfolio) <= 2:
            suggestions.append("Consider adding more holdings for better diversification")
        elif len(portfolio) > 20:
            suggestions.append("Portfolio may be too concentrated - consider reducing to 10-15 holdings")
            suggestions.append("Review each position for contribution to overall portfolio")
        
        # Suggest specific sectors if portfolio is heavily concentrated in one sector
        if sum(70 for _ in self._get_highest_sector_percentage(portfolio)):
            suggestions.append("Consider diversifying into other sectors to reduce concentration risk")
            suggestions.append("Look into mutual funds or ETFs for broad exposure")

        suggestions.extend([
            "Regular portfolio reviews every 6 months",
            "Consider dollar-cost averaging for new positions",
            "Stay informed about sector trends and economic conditions",
            "Regularly rebalance to maintain target allocations"
        ])
        
        return suggestions[:5]  # Return up to 5 suggestions

    def _get_sector_percentage(self, portfolio: Dict[str, float], sector_keywords: list, combined_str: str) -> float:
        """Calculate percentage allocation to specific sectors"""
        # Simplified approach - would need more comprehensive sector mapping
        return portfolio.get(combined_str, 0) if combined_str in portfolio else 0.0

    def _check_sector_concentration(self, portfolio: Dict[str, float]) -> str:
        """Check if portfolio has sector concentration risk"""
        # Simplified - would need more comprehensive sector mapping
        if len(portfolio) <= 2:
            return "High"
        elif len(portfolio) <= 4:
            return "Moderate"
        return "Low"

    def _get_highest_sector_percentage(self, portfolio: Dict[str, float]) -> list:
        """Get list of highest sector holdings"""
        # Simplified - would need more comprehensive sector mapping
        if len(portfolio) <= 2:
            return [key for key in portfolio.keys()]
        return portfolio.keys()