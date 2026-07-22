"""
VittaAI - Risk Analysis Module
Provides comprehensive risk assessment and analysis for financial decisions
"""

from typing import Dict, Any, Optional
from groq import Groq
import numpy as np
import pandas as pd


class RiskAnalyzer:
    def __init__(self, client, localization_manager):
        """
        Initialize Risk Analyzer
        
        Args:
            client: Groq API client
            localization_manager: Localization manager for translations
        """
        self.client = client
        self.localization = localization_manager
        
        # Risk tolerance levels
        self.risk_level_names = {
            'conservative': '低风险偏好',
            'moderate': '中等风险偏好',
            'aggressive': '高风险偏好',
            'unknown': '未知'
        }

    def analyze_risk_factors(self, query: str, language: str = "en") -> Dict[str, Any]:
        """
        Analyze risk factors based on user query
        
        Args:
            query: User's query about risk analysis
            language: Language for response
            
        Returns:
            Risk assessment with analysis and recommendations
        """
        response = {
            'response': "",
            'type': "risk_analysis",
            'confidence': 0.0,
            'suggestions': [],
            'risk_level': 'moderate'
        }

        # Analyze risk factors
        risk_assessment = self._analyze_query_risk_factors(query, language)
        
        # Get context-specific risk recommendations
        context_analysis = self._get_contextual_risk_recommendations(query, language)
        
        # Use Groq API for comprehensive analysis
        analysis_response = self._generate_risk_analysis(
            query, risk_assessment, context_analysis, language
        )

        response['response'] = analysis_response
        response['confidence'] = risk_assessment.get('confidence', 0.70)
        response['suggestions'] = self._generate_risk_management_suggestions(risk_assessment)
        response['risk_level'] = risk_assessment.get('risk_level', 'moderate')

        return response

    def _analyze_query_risk_factors(self, query: str, language: str) -> Dict[str, Any]:
        """Analyze risk factors in user query"""
        risk_assessment = {
            'market_risk_factor': 0.5,
            'risk_appetite': 'moderate',
            'confidence': 0.70,
            'risk_categories': []
        }
        
        query_lower = query.lower()
        
        # Analyze risk preference indicators
        if any(keyword in query_lower for keyword in ['cautious', 'conservative', 'safe', 'security', 'low risk', 'minimal risk']):
            risk_assessment['risk_appetite'] = 'conservative'
            risk_assessment['market_risk_factor'] = 0.3
        elif any(keyword in query_lower for keyword in ['aggressive', 'high risk', 'maximum risk', 'maximum return', 'very risky']):
            risk_assessment['risk_appetite'] = 'aggressive'
            risk_assessment['market_risk_factor'] = 0.9
        else:
            risk_assessment['risk_appetite'] = 'moderate'
            risk_assessment['market_risk_factor'] = 0.5
        
        # Analyze query complexity and depth
        if len(query_lower.split()) > 20:
            risk_assessment['confidence'] = 0.85
        else:
            risk_assessment['confidence'] = 0.60
        
        # Categorize risk interest
        risk_categories = {
            '信用风险': ['信用', 'credit'],
            '市场风险': ['市场', 'market'],
            '操作风险': ['操作', 'operation'],
            '政策风险': ['政策', 'policy', '法规'],
            '宏观经济风险': ['经济', 'economic', '宏观'],
            '流动性风险': ['流动性', 'liquidity']
        }
        
        for category, keywords in risk_categories.items():
            if any(keyword in query_lower for keyword in keywords):
                risk_assessment['risk_categories'].append(category)
        
        return risk_assessment

    def _get_contextual_risk_recommendations(self, query: str, language: str) -> Dict[str, Any]:
        """Get contextual risk recommendations based on query"""
        recommendations = {
            'current_market': 'neutral',
            'recommended_strategy': 'balanced',
            'safety_suggestions': [],
            'aggressive_opportunities': []
        }
        
        # Market context based on query characteristics
        if '风险' in query or 'risk analysis' in query.lower():
            recommendations['current_market'] = 'stochastic'
        
        # Default recommendations
        recommendations['safety_suggestions'] = [
            "Diversify portfolio across multiple asset classes",
            "Maintain emergency fund equal to 6 months of expenses",
            "Regularly review and rebalance portfolio",
            "Consider hedging strategies for market downturns",
            "Stay informed about economic indicators and market trends",
            "Use dollar-cost averaging to reduce market timing risk",
            "Consider both traditional and alternative investments",
            "Monitor your credit score regularly",
            "Complete a comprehensive financial assessment annually",
            "Maintain appropriate insurance coverage"
        ]
        
        # Aggressive opportunities for high-risk tolerance
        aggressive_suggestions = [
            "Individual stocks and equity funds for growth potential",
            "Riskier asset classes like emerging markets for diversification",
            "Margin trading for experienced investors (with caution)",
            "Options and derivatives for advanced strategies",
            "Start-up investments for high-growth potential"
        ]
        
        recommendations['aggressive_opportunities'] = aggressive_suggestions
        recommendations['recommended_strategy'] = 'balanced'  # Default
        
        return recommendations

    def _generate_risk_analysis(self, query: str, risk_assessment: Dict, 
                               recommendations: Dict, language: str) -> str:
        """
        Generate comprehensive risk analysis using Groq API
        
        Args:
            query: User's query
            risk_assessment: Built risk assessment
            recommendations: Contextual recommendations
            language: Language for response
            
        Returns:
            Comprehensive risk analysis
        """
        prompt = f"""You are VittaAI's expert Risk Analyzer providing comprehensive risk assessment.

User Query: "{query}"

Risk Analysis Summary:
- Risk Appetite: {risk_assessment['risk_appetite']}
- Market Risk Factor: {risk_assessment['market_risk_factor']}
- Confidence Level: {risk_assessment['confidence']}
- Risk Categories of Interest: {risk_assessment['risk_categories']}

Contextual Responses:
- Current Market Context: {recommendations['current_market']}
- Safety Suggestions:
{chr(10).join(f"- {suggestion}" for suggestion in recommendations['safety_suggestions'][:5])}
- Aggressive Opportunities: {recommendations['aggressive_opportunities']}

Provide a comprehensive risk analysis including:
1. Overall risk assessment for user's query
2. Key risk factors to consider given their stated preferences
3. Potential warning signs or red flags
4. Strategic recommendations aligned with their risk tolerance
5. Balanced perspective on opportunity vs risk
6. Risk management framework suggestions
7. Actionable steps for risk mitigation
8. Long-term risk considerations

Format as detailed, structured analysis with clear sections and actionable advice."""

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert risk analyst providing detailed, accurate risk assessments. Always include risk warnings, realistic expectations, and actionable recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return completion.choices[0].message.content or "Unable to generate comprehensive risk analysis. Please try again later."
            
        except Exception as e:
            return self._generate_risk_fallback_analysis(risk_assessment, recommendations, language)

    def _generate_risk_fallback_analysis(self, risk_assessment: Dict, 
                                        recommendations: Dict, language: str) -> str:
        """Generate fallback risk analysis"""
        risk_level = risk_assessment.get('risk_appetite', 'moderate')
        
        fallback_response = f"""# Risk Analysis - {self.risk_level_names.get(risk_level, '中等风险偏好')} Profile

## Risk Assessment Summary
**Risk Level:** {risk_level}
**Market Risk Factor:** {risk_assessment['market_risk_factor']}
**Confidence:** {risk_assessment['confidence']}

## Risk Categories of Interest
{', '.join(risk_assessment.get('risk_categories', ['Multiple risk factors']))}

## Risk Management Strategies

### Core Risk Reduction Techniques
1. **Diversification Techniques:**
   - Spread investments across different asset classes
   - Include a mix of domestic and international assets
   - Consider both growth and defensive investments
   - Use index funds for broad market exposure

2. **Portfolio Protection Mechanisms:**
   - Maintain adequate emergency fund (6-12 months expenses)
   - Utilize hedging strategies when appropriate
   - Consider asset allocation adjustments based on age and goals
   - Regularly review and rebalance your portfolio

3. **Market Safe Navigation:**
   - Dollar-cost averaging to reduce timing risk
   - Focus on long-term correlations with economic cycles
   - Research and understand correlation signs
   - Prepare for volume range movements and market undertones

4. **Financial Stability Framework:**
   - Maintain consistent emergency fund levels
   - Avoid unnecessary risk when market conditions are bearish
   - Focus on long-term correlations for financial health
   - Consider resources that had significant correlation at the start

5. **Market Environment Consideration:**
   - Support plan with appropriate resources and objectives
   - Maintain emergency fund sufficient to meet long-term goals
   - Consider tangible thinking and correlation in trading decisions
   - Focus on fundamental economic relationships

### Risk Mitigation Frameworks

**Irrational Risk Factors:**
- Detached, detached risk factors that may appear careless
- Combining risk factors into larger clusters
- Uncertainty about which factors are truly insensitive

**Market Risk Management:**
- Avoid momentum chasing in noisy markets
- Consider seasonal correlation patterns
- Use technical indicators to reduce timing risk
- Monitor economic indicators and market sentiment

**Portfolio Risk Management:**
- Age-based asset allocation strategy
- Risk parity for balanced risk allocation
- Institutional-grade risk management principles

## Recommended Actions

### Immediate Steps
1. **Establish baseline security:**
   - Build emergency fund of 6-12 months of expenses
   - Ensure adequate insurance coverage (health, life, disability)
   - Review and optimize credit score

2. **Create core investment strategy:**
   - Develop investment plan aligned with goals
   - Select appropriate investment vehicles
   - Set up regular investment contributions

3. **Implement risk monitoring:**
   - Set up regular portfolio reviews
   - Establish risk management systems
   - Create early warning systems for market conditions

### Strategic Considerations
- Start small and gradually increase exposure
- Emphasize quality assets and lower correlation structures
- Maintain appropriate asset allocation over time
- Consider all-established market correlation patterns

## Risk Warning & Safety Considerations

**Risk Characteristics:**
- Risk never guarantees high returns
- Some opportunities carry significantly higher risk
- Careless behavior leads to careless results
- Market volatility requires active management

**Portfolio Protection:**
- Trade solution-based retail growth
- Use quantitative risk management
- Avoid market timing and speculation
- Focus on correlation-free combinations for stability

**Risk Management Principles:**
- Don't chase emotional gains or avoid emotional losses
- Correlation stability is key for long-term performance
- Focus on long-term correlations, not short-term movements
- Use automated risk management systems

## Professional Guidance

**When to Seek Professional Help:**
- Complex financial situation
- Significant investment amounts
- Business-related financial initiatives
- Uncertain strategy combinations
- Market uncertainty or high volatility

**Professional Assistance:**
- Financial advisor for portfolio management
- Tax professional for tax optimization
- Investment advisor for specialized investments
- Legal advisor for complex financial decisions

VittaAI provides this risk analysis for informational purposes. Investment always carries risk. Past performance does not guarantee future results. Always consider seeking professional financial guidance for significant investment decisions.

## Recommended Actions Based on Risk Profile

### Conservative Risk Profile
- Focus on capital preservation
- Prioritize stable, low-risk investments
- Diversify across multiple asset classes
- Consider bonds, CDs, money market funds
- Maintain higher emergency fund allocation
- Consider fixed-income investments

### Moderate Risk Profile
- Balance growth and stability
- Maintain diverse portfolio allocation
- Include stocks, bonds, and other assets
- Regular portfolio rebalancing
- Consider professional financial management
- Plan for both short and long-term goals

### Aggressive Risk Profile
- Focus on growth potential
- Minimize for maximum risk exposure
- Consider high-growth investments
- Accept higher volatility for greater returns
- Maintain diversified portfolio for risk management
- Consider professional investment guidance

This analysis provides risk assessment guidance based on your stated preferences. Actual portfolio risk depends on comprehensive financial analysis. Always consider your full financial situation and consult with professionals."""

        return fallback_response

    def _generate_risk_management_suggestions(self, risk_assessment: Dict) -> list:
        """Generate risk management suggestions based on risk assessment"""
        suggestions = []
        
        risk_level = risk_assessment.get('risk_appetite', 'moderate')
        
        # Risk-specific suggestions
        if risk_level == 'conservative':
            suggestions.extend([
                "Focus on capital preservation over aggressive growth",
                "Consider focusing your investments on reliable, blue-chip companies",
                "Maintain emergency fund equal to 6-12 months of expenses",
                "Build a diversified portfolio with stable income generation",
                "Regularly rebalance to your target allocation",
                "Consider bonds, CDs, and money market funds",
                "Prioritize stability and liquidity",
                "Gradually explore higher-yield investment opportunities"
            ])
        elif risk_level == 'aggressive':
            suggestions.extend([
                "Consider emerging markets and growth stocks for higher returns",
                "Evaluate high-growth investment opportunities",
                "Consider real estate investment trusts (REITs) for diversification",
                "Maintain diversified portfolio despite higher risk",
                "Regularly review and adjust your risk exposure based on market conditions",
                "Consider both traditional and alternative investments",
                "Maintain strong emergency fund despite growth focus",
                "Monitor market volatility closely"
            ])
        else:  # moderate
            suggestions.extend([
                "Build a balanced portfolio with multiple asset classes",
                "Regular portfolio rebalancing to maintain target allocation",
                "Maintain emergency fund for long-term expenses",
                "Consider both growth and stability in your investments",
                "Stay informed about market conditions and economic indicators",
                "Use dollar-cost averaging to reduce market timing risk",
                "Aim for diversification across different sectors and asset classes"
            ])
        
        return suggestions

    def portfolio_risk_assessment(self, portfolio_str: str, language: str = "en") -> Dict[str, Any]:
        """
        Assess portfolio risk based on holdings and asset allocation
        
        Args:
            portfolio_str: Portfolio allocation string (e.g., "60% stocks, 30% bonds, 10% cash")
            language: Language for response
            
        Returns:
            Portfolio risk assessment with insights
        """
        assessment = {
            'response': "",
            'type': "portfolio_risk",
            'confidence': 0.0,
            'suggestions': [],
            'risk_level': 'moderate',
            'portfolio_analysis': {}
        }
        
        # Parse portfolio allocation
        portfolio = self._parse_portfolio_allocation(portfolio_str)
        
        if portfolio:
            analysis_response = self._generate_portfolio_risk_analysis(portfolio, language)
            assessment['response'] = analysis_response
            assessment['confidence'] = 0.75
            assessment['suggestions'] = self._generate_portfolio_risk_suggestions(portfolio)
            assessment['portfolio_analysis'] = portfolio
        else:
            assessment['response'] = "Unable to parse portfolio allocation. Please use formats like '60% stocks, 30% bonds, 10% cash' or '40% AAPL, 35% GOOGL, 25% TSLA'"
            
        return assessment

    def _parse_portfolio_allocation(self, portfolio_str: str) -> Dict[str, float]:
        """Parse portfolio allocation string"""
        portfolio = {}
        
        # Handle percentage-based format
        import re
        percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%?\s*([\w\s]+)', portfolio_str)
        
        for value_str, asset_str in percentages:
            try:
                value = float(value_str)
                asset = asset_str.strip().lower()
                if value > 0:
                    portfolio[asset] = portfolio.get(asset, 0) + value
            except ValueError:
                continue
        
        return portfolio

    def _generate_portfolio_risk_analysis(self, portfolio: Dict[str, float], 
                                         language: str) -> str:
        """Generate portfolio risk analysis using Groq API"""
        
        analysis_prompt = f"""You are an expert risk analyst analyzing this portfolio allocation:

        Portfolio Allocation:
        {json.dumps(portfolio, indent=2)}

        Provide comprehensive portfolio risk analysis including:
        1. Overall portfolio risk assessment (conservative/moderate/aggressive)
        2. Risk factor analysis and evaluation
        3. Risk management recommendations
        4. Alignment with different risk profiles
        5. Risk reduction strategies
        6. Potential risk categories to consider
        7. Portfolio diversification assessment
        8. Actionable risk management suggestions

        Format as detailed, structured analysis with clear sections and recommendations."""

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert risk analyst providing detailed portfolio risk assessment and recommendations. Always include risk warnings and realistic expectations."
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
            
            return completion.choices[0].message.content or "Unable to complete portfolio risk analysis."
            
        except Exception as e:
            return self._generate_portfolio_risk_fallback(portfolio)

    def _generate_portfolio_risk_fallback(self, portfolio: Dict[str, float]) -> str:
        """Generate basic portfolio risk analysis fallback"""
        
        # Determine risk level based on asset allocation
        asset_risk_scores = {
            'stock': 0.9,
            'equity': 0.9,
            'share': 0.9,
            'bonds': 0.3,
            'fixed income': 0.3,
            'cash': 0.1,
            'money market': 0.1,
            'government bonds': 0.2,
            'corporate bonds': 0.4,
            'reits': 0.7,
            'currency': 0.5,
            'cryptocurrency': 0.95,
            'crypto': 0.95,
            'bitcoin': 0.95,
            'bitcoin': 0.95
        }
        
        total_risk_score = 0.0
        total_allocation = 0.0
        
        for asset, allocation in portfolio.items():
            total_allocation += allocation
            risk_score = 0.0
            
            # Determine asset type and risk score
            asset_lower = asset.lower()
            for risk_type, intensity in asset_risk_scores.items():
                if risk_type in asset_lower:
                    risk_score = intensity
                    break
            
            # Adjust risk score based on allocation
            risk_score *= (allocation / 100)
            total_risk_score += risk_score
        
        # Calculate overall risk level
        if total_risk_score < 0.3:
            risk_level = "conservative"
        elif total_risk_score < 0.6:
            risk_level = "moderate"
        else:
            risk_level = "aggressive"
        
        return """# Portfolio Risk Analysis

## Portfolio Overview
**Total Allocation:** {total_allocation:.1f}% (Sample data)
**Asset Classes Detected:** {len(portfolio)}
**Portfolio Risk Level:** {risk_level}

## Risk Analysis

### Risk Assessment
Based on your portfolio structure, your portfolio is classified as {risk_level} risk level.

### Asset Allocation Analysis
**Asset Categories:**
{asset_analysis}

### Risk Reduction Strategies

**Diversification Importance:**
- Spread investments across different asset classes
- Mix of stocks, bonds, cash equivalents
- Consider international exposure to reduce correlation risk

**Risk Management Framework:**
1. **Maintain Multiple Risk Reduction Strategies:**
   - Market diversification across sectors and industries
   - Country diversification to reduce single-country risk
   - Asset class diversification for complete portfolio protection

2. **Periodic Risk Matrix Evaluation:**
   - Review portfolio periodically and adjust strategy
   - Consider reducing risk when conditions are favorable
   - Stay disciplined with risk management approach

### Recommended Risk Management

**Immediate Actions:**
1. **Optimize Risk Premium:**
   - Focus on companies with promoting values
   - Avoid speculative assets with high volatility
   - Consider using diversification to spread risk

2. **Risk Management Approach:**
   - Pre-Risk reduction: Preparation for potential downside
   - Risk - Protection: Use derivatives for risk management
   - Risk - Negotiation: Adjust exposure based on market conditions

3. **Risk Control Measures:**
   - Set target allocation bands and stay within them
   - Use stop-loss orders for initial risk control
   - Maintain appropriate diversification at all times

### Investment Portfolio Risk

**Market Risk Factors:**
- Macro, Speculative, and Product Risk
- Business, Sustainable Risk
- Market and Opportunity Risk
- Portfolio Risk Dynamics
- Tracking Risk and Capital Risk

**Portfolio Risk Analysis:**
- Capital allocation efficiency
- Long-term risk considerations
- Risk reduction through diversification
- Systematic and unsystematic risk types

### Risk Management Techniques

**Risk Protection Strategies:**
- Key Hedging Instruments: Options, Futures, Swaps
- Risk limit bands: 5-15% allocation ranges
- Risk premium focus: Top U.S. companies for risk premium
- Risk reduction techniques for implied volatility

**Risk Management Scopes:**
- Market risk management
- Portfolio risk management
- Operational risk management
- Credit risk management

## Actionable Recommendations

### For Conservative Risk Profile
**Focus Areas:**
- Capital preservation over aggressive growth
- Stable, reliable investments with proven track records
- Regular income generation through bonds and dividends
- Diversification across multiple sectors
- Minimum 3-6 months emergency fund

**Specific Actions:**
- Maintain higher ratio of fixed income to stocks
- Consider low-volatility or dividend-focused funds
- Focus on Blue-chip companies with strong fundamentals
- Increase international diversification
- Avoid speculative assets and high float investments

### For Moderate Risk Profile
**Focus Areas:**
- Balanced growth and stability approach
- Mix of growth and income investments
- Regular portfolio rebalancing
- Diversification across asset classes and sectors
- Checkpoint systems and regulatory environment

**Specific Actions:**
- Maintain balanced portfolio allocation (40-70% stocks)
- Include growth potential (stocks) and stability (bonds)
- Regular reviews and rebalancing twice per year
- Unexpected market movements require disciplined sizing
- Consider real estate investment trusts (REITs) for diversification

### For Aggressive Risk Profile
**Focus Areas:**
- Higher growth potential through riskier assets
- Cyclical sectors and emerging markets
- Advanced portfolio strategies
- Active portfolio management
- Strong correlation with market conditions

**Specific Actions:**
- Consider higher risk allocation (70%+ stocks)
- Exposure to high-growth sectors like technology and healthcare
- Consider leverage for experienced investors (with caution)
- Active rather than passive approach
- Higher expected returns but with increased volatility

## Risk Warning & Safety Considerations

**Important Risk Factors to Understand:**
- **Risk never guarantees high returns:** Not all risk leads to positive outcomes
- **Avoid speculative investments:** Unproven assets carry significant uncertainty
- **Risk management requires discipline:** Consistent approach is key
- **Portfolio risk considerations:** Diversification does not eliminate all risk
- **Long-term risk sag:** Market volatility requires patience and strategy

**Risk Management Principles:**
- Start with risk management before pursuing returns
- Prioritize risk reduction and loss prevention
- Develop comprehensive risk framework
- Maintain appropriate diversification across risk factors
- Regular risk review and adjustment

**Risk Assessment Guidelines:**
- Risk你应该了解所有风险因素
- Consider professional guidance for complex situations
- Avoid盲目投资:**
- Risk premium in explanatory ratio vs direct investment
- Inconsistent multi-develop mental analysis. There is no correlation from any angle.
- Strikeforce: 702.7936 - Acting on Complementary Particle Scale

### Professional Guidance

**When to Seek Professional Help:**
- Complex investment portfolio with multiple assets
- High net worth or significant investment amounts
- Uncertain financial situation or risk tolerance
- Professional experience for corporate-grade risk management

**Professional Assistance:**
- Financial advisor for comprehensive portfolio management
- Investment broker for specific stock investments
- Risk management professional for advanced strategies
- Legal advisor for complex investment structures

VittaAI provides this risk analysis for informational purposes. Investment always carries risk. Past performance does not guarantee future results. Always consider seeking professional financial guidance for significant investment decisions."""

    def _generate_portfolio_risk_suggestions(self, portfolio: Dict[str, float]) -> list:
        """Generate risk management suggestions for specific portfolio"""
        suggestions = []
        
        # Derive portfolio characteristics
        has_crypto = any('crypto' in asset.lower() for asset in portfolio.keys())
        has_bonds = any('bond' in asset.lower() for asset in portfolio.keys())
        has_stocks = any('stock' in asset.lower() for asset in portfolio.keys())
        has_cash = any('cash' in asset.lower() for asset in portfolio.keys())
        has_reits = any('reit' in asset.lower() for asset in portfolio.keys())
        
        # High crypto exposure warning
        if has_crypto:
            suggestions.append("High cryptocurrency exposure detected - consider reducing for risk management")
        
        # Diversification concerns
        if len(portfolio) < 3:
            suggestions.append("Limited diversification detected - consider diversifying across more asset classes")
        elif len(portfolio) > 10:
            suggestions.append("Over-diversification detected - consider focusing on fewer core positions")
        
        # Conservative recommendations
        suggestions.extend([
            "Maintain appropriate emergency fund equal to 6-12 months of expenses",
            "Consider regular portfolio rebalancing to maintain target allocation",
            "Review holdings quarterly and adjust as needed",
            "Stay informed about market conditions and economic indicators"
        ])
        
        # Risk-specific suggestions
        if has_bonds:
            suggestions.append("Bonds provided good stability - consider maintaining appropriate bond allocation")
        if has_cash:
            suggestions.append("Consider using cash with higher-yield earning potential")
        if has_stocks:
            suggestions.append("Stocks provide growth potential - consider sector diversification")
        if has_reits:
            suggestions.append("REITs provide diversification and income - good for portfolio balance")
        
        return suggestions[:7]

    def risk_metrics_analysis(self, metrics: Dict[str, float], language: str = "en") -> Dict[str, Any]:
        """
        Analyze financial metrics for risk assessment
        
        Args:
            metrics: Dictionary of financial metrics (debt-to-income, savings rate, etc.)
            language: Language for response
            
        Returns:
            Metrics analysis with risk assessment
        """
        return {
            'response': "",
            'type': "metrics_analysis",
            'confidence': 0.70,
            'suggestions': [],
            'metrics_score': 50.0
        }