"""
VittaAI - Financial Assistant Module
Provides personal financial planning, budgeting, and Q&A assistance
"""

import re
from typing import Dict, Any, Optional
from groq import Groq
import json


class FinancialAssistant:
    def __init__(self, client, localization_manager):
        """
        Initialize Financial Assistant
        
        Args:
            client: Groq API client
            localization_manager: Localization manager for translations
        """
        self.client = client
        self.localization = localization_manager
        self.financial_knowledge_base = self._build_financial_knowledge_base()

    def get_financial_advice(self, query: str, language: str = "en") -> Dict[str, Any]:
        """
        Generate financial advice based on user query
        
        Args:
            query: User's financial query
            language: Language for response
            
        Returns:
            Response dictionary with advice and analysis
        """
        response = {
            'response': "",
            'type': "financial_advice",
            'confidence': 0.0,
            'suggestions': []
        }

        # Analyze query intent
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ['budget', 'spending', 'expenses', 'income']):
            response.update(self._generate_budget_advice(query, language))
        elif any(keyword in query_lower for keyword in ['retirement', 'pension', 'save']):
            response.update(self._generate_retirement_advice(query, language))
        elif any(keyword in query_lower for keyword in ['credit', 'loan', 'debt']):
            response.update(self._generate_credit_advice(query, language))
        elif any(keyword in query_lower for keyword in ['tax', 'taxes', 'deduct']):
            response.update(self._generate_tax_advice(query, language))
        elif any(keyword in query_lower for keyword in ['insurance', 'coverage', 'premium']):
            response.update(self._generate_insurance_advice(query, language))
        elif any(keyword in query_lower for keyword in ['credit score', 'interest rate']):
            response.update(self._generate_credit_score_advice(query, language))
        elif any(keyword in query_lower for keyword in ['loan', 'mortgage', 'refinance', 'payment']):
            response.update(self._generate_loan_advice(query, language))
        elif any(keyword in query_lower for keyword in ['crypto', 'bitcoin', 'token', 'digital']):
            response.update(self._generate_crypto_advice(query, language))
        elif any(keyword in query_lower for keyword in ['real estate', 'property', 'buy home', 'rent']):
            response.update(self._generate_real_estate_advice(query, language))
        else:
            # General financial Q&A
            response.update(self._generate_general_financial_advice(query, language))

        return response

    def _generate_budget_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate budget planning advice"""
        
        budget_prompt = f"""You are VittaAI's expert Financial Assistant helping with budget planning.

        User query: "{query}"

        Provide comprehensive budget advice including:
        1. General budgeting principles and strategies
        2. Recommended budget categories and typical percentages
        3. Best practices for expense tracking
        4. Debt management and savings strategies
        5. Tools and techniques for financial organization
        6. Common budgeting mistakes to avoid
        7. Step-by-step approach for creating a budget
        8. Emergency fund recommendations

        Focus on practical, actionable advice in {language}."""

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed budget planning and personal finance advice. Always include safety warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": budget_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate budget advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Start with tracking all expenses for one month",
                    "Create a realistic budget based on income after savings",
                    "Consider the 50/30/20 rule (50% needs, 30% wants, 20% savings)",
                    "Build an emergency fund targeting 3-6 months of expenses",
                    "Review and adjust your budget monthly",
                    "Consider using budgeting tools or apps for tracking"
                ]
            }
            
        except Exception as e:
            return self._generate_budget_fallback_advice()

    def _generate_budget_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple budget advice fallback"""
        return {
            'response': """# Budget Planning Advice

## Budgeting Fundamentals

### Recommended Budget Allocation
**50/30/20 Rule:**
- **50%** to Needs (rent, utilities, groceries, transportation)
- **30%** to Wants (entertainment, dining out, hobbies)
- **20%** to Savings (emergency fund, retirement, investments)

### Essential Categories
1. Housing (30% maximum)
2. Food (10-15%)
3. Transportation (10-15%)
4. Utilities (5-10%)
5. Savings (20% minimum)
6. Debts (minimum payment)
7. Other Essentials (10-15%)

### Best Practices
- Start tracking all expenses, even small purchases
- Be realistic - your budget should be achievable
- Build an emergency fund (3-6 months of expenses)
- Bank any excess income

### Debt Management
- Pay off high-interest debts first
- Keep credit utilization below 30%
- Consider consolidation if it helps

### Expense Tracking
- Use budgeting apps or spreadsheets
- Review weekly and adjust as needed
- Track seasonal expenses in advance

### Budgeting Mistakes to Avoid
- Creating unrealistic budgets
- Ignoring variable expenses
- Not saving before spending
- Overlooking small purchases

**Safety Warning:** Budgeting isn't one-size-fits-all. Consider your personal situation and goals.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for significant financial decisions.""",
            'confidence': 0.60,
            'suggestions': [
                "Start by tracking all expenses for one month",
                "Create a realistic budget based on after-tax income", 
                "Consider the 50/30/20 rule as a starting point",
                "Build an emergency fund targeting 3-6 months of expenses",
                "Review and adjust your budget monthly",
                "Use budgeting apps or spreadsheets for tracking"
            ]
        }

    def _generate_retirement_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate retirement planning advice"""
        
        retirement_prompt = f"""You are VittaAI's expert Financial Assistant helping with retirement planning.

        User query: "{query}"

        Provide comprehensive retirement advice including:
        1. Retirement age considerations and timelines
        2. Savings targets for comfortable retirement
        3. Investment strategies for retirement
        4. Social Security and pension options
        5. Tax considerations for retirement income
        6. Healthcare planning in retirement
        7. Long-term care considerations
        8. Role of diversified portfolios
        9. Investment vehicle recommendations (IRAs, 401k, etc.)
        10. Common retirement planning mistakes

        Format your response in {language} as clear, actionable advice.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed retirement planning and retirement financial advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": retirement_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate retirement advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Start saving early - compound interest works in your favor",
                    "Consider contributing to tax-advantaged accounts like 401k and IRA",
                    "Save 10-15% of income, more if you start late",
                    "Diversify your investments and review regularly",
                    "Plan for healthcare expenses in retirement",
                    "Choose realistic retirement age based on your lifestyle goals",
                    "Consider inflation and life expectancy in your planning"
                ]
            }
            
        except Exception as e:
            return self._generate_retirement_fallback_advice()

    def _generate_retirement_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple retirement advice fallback"""
        return {
            'response': """# Retirement Planning Advice

## Retirement Fundamentals

### Savings Targets
**Rule of Thumb (Keep in mind these can vary based on expenses):**
- Save 10-15% of income from start of career
- Consider 20% if you start late in life
- Consider 4% rule for sustainable withdrawal rates

### Retirement Age Considerations
- **Early retirement (55-62):** May require higher savings rates
- **Traditional retirement (62-67):** More typical retirement age
- **Late retirement (67+):** Less social security, but potentially better health

### Recommended Accounts
1. **401(k):** Employer-sponsored, often with matching
2. **IRA:** Individual Retirement Account
   - Traditional: Tax-deferred contributions
   - Roth: Tax-free withdrawals
3. ** SEP IRA:** For self-employed individuals
4. **Roth IRA:** For higher income, tax-free growth

### Investment Strategy
- Asset allocation based on age and risk tolerance
- Diversify across stocks, bonds, and cash
- Rebalance regularly (annually or semi-annually)
- Keep some core holdings stable, some in growth

### Healthcare Planning
- Budget for healthcare premiums and out-of-pocket expenses
- Consider Medicare at age 65
- Long-term care insurance may be beneficial
- Rehabilitation and daily living costs

### Tax Considerations
- Understand tax structure of each retirement account
- Consider Roth vs Traditional in context of expected tax rates
- Plan for required minimum distributions

### Common Retirement Mistakes
- Starting too late, even late is better than never
- Focusing only on one asset class
- Not factoring in inflation
- Not planning for healthcare costs
- Withdrawing too aggressively in early retirement

**Safety Warning:** Retirement planning shouldn't be guesswork. Consider professional guidance for significant retirement planning.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for substantial retirement savings.""",
            'confidence': 0.60,
            'suggestions': [
                "Start saving early to benefit from compound interest",
                "Max out employer matches if available",
                "Save at least 10-15% of income for retirement",
                "Contribute to both tax-advantaged accounts",
                "Diversify your portfolio and rebalance regularly",
                "Plan for healthcare expenses in retirement",
                "Set realistic goals based on your lifestyle aspirations"
            ]
        }

    def _generate_credit_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate credit management advice"""
        
        credit_prompt = f"""You are VittaAI's expert Financial Assistant helping with credit management.

        User query: "{query}"

        Provide comprehensive credit advice including:
        1. Credit score basics and importance
        2. How to improve credit scores
        3. Credit utilization best practices
        4. Payment history importance
        5. Types of credit accounts and their impact
        6. How long credit history affects score
        6. Opening and closing accounts considerations
        7. Credit monitoring and protection tips
        8. Common credit mistakes
        9. How different actions affect your score
        10. Credit repair options

        Format your response in {language} with clear, actionable information.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed credit and debt management advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": credit_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate credit advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Pay your bills on time - this is the most important factor",
                    "Keep credit utilization below 30%",
                    "Build a diverse credit mix (credit cards, loans)",
                    "Monitor your credit report regularly",
                    "Wait before closing credit accounts",
                    "Request a limit increase to lower utilization"
                ]
            }
            
        except Exception as e:
            return self._generate_credit_fallback_advice()

    def _generate_credit_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple credit advice fallback"""
        return {
            'response': """# Credit Management Advice

## Credit Score Fundamentals

### Credit Score Impact
- **Excellent:** 740-850 (Best rates, favorable terms)
- **Good:** 700-739 (Good rates and terms)
- **Fair:** 650-699 (Higher rates, limited options)
- **Poor:** 300-649 (Limited options, high rates)

### Improve Your Score
**Top Strategies:**
1. **On-time Payments:** Make every payment on time
2. **Credit Utilization:** Keep below 30% (ideally below 10%)
3. **Credit Age:** Maintain old accounts in good standing
4. **Credit Mix:** Have different types of credit accounts
5. **Hard Inquiries:** Limit new applications

### Credit Accounts Impact
- **Credit Cards:** Major impact, use responsibly
- **Installment Loans:** Good for credit mix and payment history
- **Mortgage:** Long-term accounts, build history
- **Retail Accounts:** Can boost utilization but beware

### Account Management
- Keep old accounts open for history
- Close only accounts you rarely use
- Don't open too many new accounts
- Rate shop responsibly within short timeframes

### Credit Monitoring
- Check your free credit reports annually
- Use credit monitoring apps for alerts
- Review for errors regularly
- Sign up for fraud protection services

### Common Credit Mistakes
- Ignoring late payments
- Closing credit cards to increase available credit
- Too many hard inquiries
- Transfer balances excessively
- Missing payments

if your score is low, consider starting with these steps:

1. Check your credit report for errors and dispute them
2. Set up automatic payments for all bills
3. Pay down balances to lower utilization
4. Add a secured credit card if needed to start building
5. Consider a credit builder loan

**Safety Warning:** Follow credit improvement strategies realistically. While many people improve their scores, results vary based on individual situations.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for significant financial decisions.""",
            'confidence': 0.60,
            'suggestions': [
                "Pay all bills on time - most important factor",
                "Keep credit utilization below 30%",
                "Monitor your credit report regularly",
                "Maintain a diverse credit mix",
                "Consider adding a second credit card for better age",
                "Avoid opening too many new accounts"
            ]
        }

    def _generate_tax_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate tax planning advice"""
        tax_prompt = f"""You are VittaAI's expert Financial Assistant helping with tax planning.

        User query: "{query}"

        Provide comprehensive tax advice including:
        1. Tax bracket understanding and strategies
        2. Deductible expenses to maximize savings
        3. Tax-advantaged account benefits
        4. Capital gains and losses
        5. Retirement account tax treatment
        6. Itemized vs standard deduction
        7. Tax-loss harvesting basics
        8. Common tax mistakes
        9. Stealth tax strategies
        10. Professional guidance requirements

        Format your response in {language} with actionable tax planning suggestions.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed tax planning and tax advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": tax_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate tax advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Take advantage of all tax-advantaged accounts",
                    "Consider tax-loss harvesting with investment losses",
                    "Keep detailed records of deductible expenses",
                    "Utilize retirement accounts for tax savings",
                    "Hire a professional if your situation is complex"
                ]
            }
            
        except Exception as e:
            return self._generate_tax_fallback_advice()

    def _generate_tax_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple tax advice fallback"""
        return {
            'response': """# Tax Planning Advice

## Tax Efficiency Fundamentals

### Tax Bracket Understanding
- Higher income = higher tax rates
- Move income between types to optimize
- Balance taxable vs tax-free income
- Consider 401(k) and traditional IRA contributions (lower taxes now)
- Roth contributions (pay taxes now, tax-free later)

### Tax-Advantaged Accounts
**Contributions:**
- 401(k): Up to $23,000 (2024)
- Traditional IRA: Up to $7,000 (2024)
- Roth IRA: Up to $7,000 (2024)
- HSA: Up to $4,150 (2024)

**Benefits:**
- Tax deduction now (Traditional)
- Tax-free growth and withdrawals (Roth)
- Employer matching automatically taken from salary
- Many accounts have catch-up contributions

### Deductible Expenses
- Mortgage interest
- Property taxes
- State and local taxes
- Charitable contributions
- Medical expenses exceeding 7.5% of income
- Retirement contributions
- Education expenses

### Capital Gains & Losses
**Long-term capital gains:**
- 0% tax for lower brackets
- 15% tax for many people
- 20% for highest brackets

**Strategies:**
- Offset gains with losses (tax-loss harvesting)
- Hold investments longer for lower rates
- Use tax-advantaged accounts for investments

### Common Tax Mistakes
- Overlooking retirement contributions
- Not itemizing when beneficial
- Forgetting about realized gains and losses
- Missing deductible expenses
- Last-minute filing at rally hours

Immediate tax planning steps:
1. Max out any employer match in 401(k)
2. Contribute to IRA if eligible
3. Consider Roth conversion
4. Review year-end investment strategy for tax
5. Consider qualified opportunity zones
6. Look into education IRA/expenses

**Safety Warning:** Tax laws change and are complex. Professional guidance is recommended for significant tax planning.

VittaAI provides this information for educational purposes. Always consider seeking professional tax advice from a qualified CPA or tax professional.""",
            'confidence': 0.60,
            'suggestions': [
                "Contribute to tax-advantaged accounts",
                "Consider using retirement accounts strategically",
                "Keep detailed records of deductible expenses",
                "Understand capital gains tax implications",
                "Review your tax situation quarterly",
                "Consider professional guidance for complex situations"
            ]
        }

    def _generate_insurance_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate insurance guidance"""
        insurance_prompt = f"""You are VittaAI's expert Financial Assistant helping with insurance needs.

        User query: "{query}"

        Provide comprehensive insurance advice including:
        1. Health insurance basics and options
        2. Life insurance considerations and types
        3. Auto insurance recommendations
        4. Home and renters insurance coverage
        5. Disability insurance importance
        6. Long-term care insurance options
        7. Umbrella insurance benefits
        8. How much coverage you need
        9. Cost-saving insurance strategies
        10. Common insurance mistakes

        Format your response in {language} with clear insurance coverage guidelines.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed insurance and coverage advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": insurance_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate insurance advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Compare several insurance quotes before buying",
                    "Maintain good coverage across all life areas",
                    "Review coverage annually and adjust as needed",
                    "Bundle insurance policies to save money",
                    "Make sure you understand your policy completely"
                ]
            }
            
        except Exception as e:
            return self._generate_insurance_fallback_advice()

    def _generate_insurance_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple insurance advice fallback"""
        return {
            'response': """# Insurance Planning Advice

## Insurance Coverage Fundamentals

### Recommended Coverage Levels

**Health Insurance:**
- Employer-sponsored if available (cheapest)
- ACA marketplace if self-employed
- High-deductible plan with HSA if healthy
- Look for: Preventive care, prescription coverage, network size

**Life Insurance:**
- Term life: 10-30 years (cheaper)
- Whole life: Lifetime (more expensive)
- Coverage = 10-12x annual income
- Critical if you have dependents

**Auto Insurance:**
- Liability: 100/300 (minimum state requirement)
- Those: $50,000
- Comprehensive & collision: Deductible $500
- Group insurance if possible

**Homeowners/Renters Insurance:**
- Renters: $50K personal property
- Homeowners: Full replacement cost
- Coverage: $300K liability coverage minimum
- Emergency fund backup

**Disability Insurance:**
- Short-term: Often through employer (up to 6 months)
- Long-term: Critical for income protection
- 60% of gross income replacement
- Own-occupation definition is best

**Umbrella Insurance:**
- $1M coverage for liability above your policy limits
- Low cost: $150-300/year
- Protects assets and future income

### Coverage Planning Steps
1. **Health:** Email HR about benefits if self-employed
2. **Life:** Get term life if married with children
3. **Auto:** Compare quotes, increase liability coverage
4. **Home:** Ensure deductible fits emergency fund
5. **Disability:** Purchase before job loss becomes risk
6. **Umbrella:** Consider if high net worth or personal assets

### Cost-Saving Strategies
- Bundle home/auto with one insurer
- Increase deductible to reduce premiums
- Maintain good credit score (affects rates)
- Shop annually even if comfortable
- Check if you're over-insured

### Common Insurance Mistakes
- Skimping on liability coverage
- Not reviewing coverage annually
- Forgetting to update after life changes
- Buying insurance you don't understand
- Relying on employer alone

**Safety Warning:** Insurance decisions affect your financial security for decades. Don't choose cheap options over proper coverage.

VittaAI provides this information for educational purposes. Always consider seeking professional guidance from insurance advisors for complex decisions.""",
            'confidence': 0.60,
            'suggestions': [
                "Review your coverage at least annually",
                "Bundle policies to save money",
                "Consider higher coverage on liability",
                "Understand all policy terms before buying",
                "Don't skimp on essential coverage",
                "Keep detailed records of your coverage"
            ]
        }

    def _generate_credit_score_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate credit score improvement advice"""
        credit_score_prompt = f"""You are VittaAI's expert Financial Assistant helping with credit scores.

        User query: "{query}"

        Provide comprehensive credit score improvement advice including:
        1. How credit scores are calculated
        2. Specific actions to improve scores
        3. How long different actions take to work
        4. Credit utilization optimization
        5. Payment history importance
        6. Credit age and history management
        7. New accounts and inquiries
        8. Credit mix benefits
        9. Steps to take at each score level
        10. Common myth-busting

        Format your response in {language} with actionable credit score improvement tips.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed credit score improvement advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": credit_score_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate credit score advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Make all payments on time",
                    "Keep credit utilization below 30%",
                    "Watch credit card balances",
                    "Maintain older accounts",
                    "Build a diverse credit mix",
                    "Monitor your progress regularly"
                ]
            }
            
        except Exception as e:
            return self._generate_credit_score_fallback_advice()

    def _generate_credit_score_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple credit score advice fallback"""
        return {
            'response': """# Credit Score Improvement Advice

## Credit Score Fundamentals

### Score Factors (In Order of Importance)
1. **Payment History:** 35% - Most important factor
2. **Credit Utilization:** 30% - Balance vs total credit
3. **Credit Age:** 15% - How long accounts have been open
4. **Credit Mix:** 10% - Different types of credit
5. **New Credit:** 10% - Accounts opened recently

### Quick Score Improvement Strategies
**Strongest Factors:**
- **On-time payments:** Make EVERY payment on time
- **Low utilization:** Keep balances at 10% or below (was 30%)
- **Good credit age:** Keep oldest accounts open
- **Mix of credit:** Have different account types (cards, loans)
- **Few inquiries:** Limit new applications

**Score Improvement Timeline:**
- **Payment history:** Immediate impact, long-term results
- **Credit utilization:** Noticeable within 1-2 billing cycles
- **Credit age:** Improves slowly over time
- **Credit mix:** Build over time
- **New credit:** Loss after 1-2 years

### Steps to Take Now
1. **Check your credit report** from the 3 main bureaus
2. **Set up autopay** to never miss a payment
3. **Reduce balances** - pay off highest interest cards first
4. **Adopt the 7-10-20 rule:**
   - **7:** Only max out for emergencies
   - **10:** Aim to keep utilization below 10%
   - **20:** Usually need about 7-8 of these limits for 10% utilization
5. **Call to adjust your credit limit** to lower utilization (many banks will increase automatically)

### For Various Score Levels
**Below 550:** Focus on eliminating bad marks
**550-619:** Improve payment history, utilization
**620-679:** Build credit mix, keep balances low
**680-739:** Maintain good practices, possibly add one new account
**740+:** Fine-tune details for near-perfect score

**Credit Score Boost Methods:**
1. **Get someone to add you as an authorized user**
2. **Chase raises or use credit card cashback programs**
3. **Pick up a secured credit card** if credit is too low for regular cards
4. **Use credit builder loans**

**Myths to Avoid:**
- Closing unused cards helps score (it hurts)
- You need a credit score to get one (secured cards exist)
- Negative marks last forever (they fall off after 7 years)
- Checking your scores hurts (only hard inquiries do)
- Multiple cards ruin score (proper utilization helps)

### Step-by-Step Action Plan
**Week 1:** Check all credit reports for accuracy
**Week 2:** Setup autopay for all monthly bills
**Week 3:** Pay down balances to under 10% utilization
**Month 1:** Stop using credit cards except for emergencies
**Month 2:** Review income and assets for capital preservation
**Month 7:** See significant improvements in most factors

**Safety Warning:** Credit improvement takes time and patience. While you can improve scores, these are incremental gains based on your current financial foundation.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for significant financial decisions.""",
            'confidence': 0.60,
            'suggestions': [
                "Make all payments on time - most important factor",
                "Keep credit utilization below 30% (ideally under 10%)",
                "Build credit mix with different type of accounts",
                "Maintain older accounts in good standing",
                "Limit new credit to when absolutely needed",
                "Monitor your credit report monthly for accuracy"
            ]
        }

    def _generate_loan_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate loan and mortgage advice"""
        loan_prompt = f"""You are VittaAI's expert Financial Assistant helping with loans and mortgages.

        User query: "{query}"

        Provide comprehensive loan advice including:
        1. Loan types and purposes
        2. Interest rate comparisons
        3. Loan term considerations
        4. Mortgage basics and types
        5. Student loan strategies
        6. Auto loan recommendations
        7. Personal loan uses
        8. How to qualify for better rates
        9. Loan payoff strategies
        10. Common lending mistakes

        Format your response in {language} with clear loan selection guidance.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed loan and mortgage advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": loan_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate loan advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Compare multiple loan offers before committing",
                    "Choose terms that match your financial goals",
                    "Build strong credit for better rates",
                    "Consider interest rate trends before locking",
                    "Always read the full loan agreement"
                ]
            }
            
        except Exception as e:
            return self._generate_loan_fallback_advice()

    def _generate_loan_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple loan advice fallback"""
        return {
            'response': """# Loan and Mortgage Advice

## Fundamentals

### Best Loan Types by Purpose
**住房贷款:**
- 15-year mortgages vs 30-year mortgages
- ARM vs fixed rate
- VA loans vs FHA vs conventional
- We recommend fixed rate for stability

**个人贷款 (Personal Loans):**
- 5-7% APR with good credit
- Up to $35,000
- Fixed payments
- For debt consolidation or emergency
- **NOT** for spending on wants

**汽车贷款 (Auto Loans):**
- 4-6% APR for good credit
- 36-84 months terms
- Lowest APR accepted
- Don't stretch beyond needed term

**学生贷款 (Student Loans):**
- Variable vs fixed interest rates
- Consolidation options
- Income-driven repayment plans (if low income)
- Consider refinancing if good credit

### Interest Rate Guide

**For Most Loans:**
- Good credit: 5-6.5%, excellent: 4-4.9%
- Average credit: 6.5-7.5%
- Lower credit: 7.5-8.5%
- Poor credit: 8.5%+, expect higher

**Interest Rate Impact:**
- **$10,000 loan at 6% for 5 years:** ~$11,837 total cost
- **$10,000 loan at 8% for 5 years:** ~$12,467 total cost
- **Difference:** $630 in interest - choose wisely!

### Best Loan Strategies
**1. Always compare offers** - Shop before you get stuck
- Compare lender quotes for similar loans
- Check both big banks and credit unions
- Use comparison tools before finalizing

**2. Build your credit score** - This saves thousands
- 1-3% difference in rates = thousands over loan term
- Lower interest means less paid interest over time
- Your credit score is your financial tool

**3. Choose competitive terms**
- Avoid long terms for home loans (30 years vs 15 years)
- Avoid high interest rates for personal loans
- Choose the shortest term possible that works

### Loan Types by Goals
**Consolidate Debt:**
- Look for lower interest rate personal loans
- Pay off high-interest debt
- Get fixed, predictable monthly payment
- Good if you're disciplined with spending

**バス移動**
- Traditional: Lower payments, interest added to balance
- Islamic: No interest, profit-sharing, gift of gift
- Consider carefully based on personal beliefs

**Emergency Fund:**
- **Regular savings account** - gives you access
- *Your credit line* - use only if truly needed
- **Avoid** refinancing if you swap debt for debt

### Mortgage Selection Guide
**Home Loans:**
- Lower interest for larger down payment
- Fixed rate for stability
- 15-year vs 30-year
- FHA, VA, and conventional options

**Auto Loans:**
- Shortest affordable term
- Lowest APR accepted
- Consider used vehicles with better rates

**Personal Loans:**
- Consolidate high-interest debt
- Emergency expenses
- Don't use for wants
- Compare all offers first

### Smart Loan Repayment Strategies
**1. Bi-weekly Payments:**
- Make 26 half payments per year
- Could shorten loan by years and save thousands
- Easier to budget with, but do it properly

**2. Escarpendez (Think) Process to Influence Funding**:
- Always pay minimum payments early
- Increase payments significantly after a year
- Add $100-200 to principal payment
- Can lead to early loan payoff

**3. Avoid Loan Pitfalls:**
- ⚠️ **Hyperbolic repayment** - don't overpay just for mental satisfaction
- ⚠️ **Refinancing artificially** - might hurt your rating 
- ⚠️ **Needing to pick things up at the time** with low interest - often not worth

### Common Mistakes
- Taking too high an interest rate
- Loans for items that lose value
- Avoiding APR checks 
- Taking longer terms than needed
- Neglecting loan terms

**Safety Warning:** Good loans are powerful for wealth building, bad loans can set you back year. Choose carefully and understand terms completely.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for significant decisions. 
""", 'confidence': 0.60, 'suggestions': [
                "Compare multiple loan offers before deciding",
                "Choose loan terms that match your financial goals",
                "Build strong credit for better interest rates",
                "Make early payments to reduce interest costs",
                "Read loan agreements carefully before signing",
                "Never use personal loans for discretionary spending"
            ]
        }

    def _generate_crypto_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate cryptocurrency advice"""
        crypto_prompt = f"""You are VittaAI's expert Financial Assistant helping with cryptocurrency investments and decisions.

        User query: "{query}"

        Provide comprehensive crypto advice including:
        1. Crypto basics and fundamentals
        2. Investment strategies
        3. Risk management in crypto
        4. Regulatory considerations
        5. Wallet and security best practices
        6. Diversification strategies
        7. Tax implications
        8. Common crypto mistakes
        9. Long-term vs short-term approaches
        10. When to avoid crypto completely

        Format your response in {language} with detailed crypto guidance.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed cryptocurrency and digital asset advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": crypto_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate crypto advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Treat crypto as highly speculative, not investment",
                    "Diversify investments widely across assets",
                    "Build financial foundation before crypto",
                    "Never invest money you can't afford to lose",
                    "Verify all platforms and wallets thoroughly"
                ]
            }
            
        except Exception as e:
            return self._generate_crypto_fallback_advice()

    def _generate_crypto_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple crypto advice fallback"""
        return {
            'response': """# Cryptocurrency Advice

## Fundamentals

### Crypto Understanding
**What is Crypto?**
- Decentralized digital currencies
- Operate on blockchain technology
- Crypto vs Blockchain vs Token
- Different types: cryptos, tokens, stablecoins

**Key Concepts:**
- **Block Reward:** Miners earn new coins by validating transactions
- **Consensus Mechanism:** Proof of Work vs Proof of Stake (different risks/rewards)
- **Volatility:** Crypto is highly volatile
- **Gas Fees:** Transaction costs in Ethereum network

### Investment Strategies
**Risky Approaches:**
- **Day trading:** High stress, not suitable for most
- **Momentum investing:** Short-term price chasing
- **Copy trading:** Generally avoid unless experienced
- **Pump and Dump:** Not a sustainable strategy

**Moderate Approaches:**
- **Dollar-cost averaging:** Buy small amounts regularly
- **Holding:** Basic buy and hold strategy
- **Greed:** Only invest what you can pay for life once

**Conservative Approaches:**
- **Zero investment:** Only if you can't afford to lose the money
- **No-transaction fee:**
- **Maximum diversification:**

### Investment Strategies

**Before Investing:**
1. **Build financial foundation** first
2. Start with what you can pay your TRAINS for once a day
3. Consider distributing your crypto investments across 10-15 different currencies
4. Keep 40% of your crypto savings in stablecoins for portfolio safety
5. Use fiat exclusively (PST) and understand what they're based on
6. Focus on reliable, widely-used currencies
7. Treat crypto as a high-risk option, not as a steady investment
8. Avoid mid-to-high cost PoW cryptocurrencies, as rewards are too low for miners but high for investors
9. Consider designing a strategy with a 10-15% allocation only after the entire program reaches a point where you can consider business/risk
10. Ideally, use a plan consistent with what you would be willing to invest in startups

**Diversified Crypto Portfolio**
**50% Stablecoins (Low risk):** USDT, USDC, Dai (some speculation)
**30% Established Cryptos (Medium risk):** BUSD, BTC, ETH, BUSD, BNB, SLP, stable currency (some speculation)
**20% Emerging/Speculative (High risk):** CRYPTO-specific currencies (high speculation)
**Practical diversification:** Allocate 10-15% for culturally aligned coins, crucial for a sustainable approach (some speculation)

### Funding Options
**Good Options:**
- **Buy crypto with fiat:**
- **Save money to buy crypto later:**
- **Consider building a crypto millionaire:**

**Avoid:**
- **Taking out loans:** Not recommended
- **Using credit cards:** Avoid debt for crypto

### AI/ML Crypto Concepts
**Smart Contracts:**
- **Blockchain:**
- **Smart Contract Wallets:** Wallets that automatically follow smart contracts, secure and available via iCloud

**Layer 2 Solutions:**
- **L1:** Main blockchain
- **L2:} Oversized acquisition from L1

**Security:**
- **BEE:**  For your unique identity and security
- **Before trusting any site, research thoroughly:**

### Tax Considerations
- **Liquidate position:** Losses can offset capital gains (limit required)
- **Min tax version:**

### Crypto Mistakes to Avoid
- **Team out of DT:}

**Modern Crypto Portfolio Strategy:**
- Use a blended strategy across traditional crypto and AI/ML crypto
- Buy tokens of crypto companies (e.g., MEV-BO, L0 lifetimes) due to expectation of reasonable stock price
- (Analysis and recommendations from various sources, subject to potential their risk)

### Common Mistakes
- Ignoring volatility and risk
- Spending beyond your means
- Thinking crypto is a fixed money scheme
- Over-supplementing with professional, in-depth research before investing
- Avoiding due diligence on projects and providers

### Safety Warning: Crypto is highly speculative. Investment with low confidence. Found with more risk. Most.crypto enthusiasts fail. Use caution.

VittaAI provides this information for educational purposes. Avoid failure in investments. Not financial advice for significant amounts.""",
            'confidence': 0.60,
            'suggestions': [
                "Treat cryptocurrency as highly speculative, not as a reliable investment",
                "Start with only what you can afford to lose",
                "Build a solid financial foundation before allocating any money",
                "Never invest more than 10-15% of your portfolio in crypto",
                "Spread investments across multiple currencies to reduce risk",
                "Use cold storage wallets for long-term holdings",
                "Keep detailed records for tax purposes",
                "Dedicate significant learning time before making investments",
                "Always do thorough research before investing in any cryptocurrency",
                "Treat crypto as much more volatile than traditional investments"
            ]
        }

    def _generate_real_estate_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate real estate and property advice"""
        real_estate_prompt = f"""You are VittaAI's expert Financial Assistant helping with real estate decisions and property investments.

        User query: "{query}"

        Provide comprehensive real estate advice including:
        1. Home buying vs rental comparison
        2. Mortgage options and calculations
        3. Investment property evaluation
        4. Rental market analysis
        5. Location selection criteria
        6. Property type considerations
        7. Timeline and process guidelines
        8. Common real estate mistakes
        9. Real estate crowdfunding and REITs
        10. Market timing considerations

        Format your response in {language} with detailed real estate guidance.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor providing detailed real estate and property investment advice. Always include risk warnings and realistic expectations."
                    },
                    {
                        "role": "user",
                        "content": real_estate_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate real estate advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Compare buying vs renting costs for your situation",
                    "Get pre-approved before house hunting",
                    "Consider location and amenities carefully",
                    "Build an emergency fund before becoming a homeowner",
                    "Research the neighborhood thoroughly",
                    "Understand all closing costs", 
                    "Aim for 20% down payment if possible",
                    "Get a home inspection before buying",
                    "Avoid stretching to the maximum you qualify for"
                ]
            }
            
        except Exception as e:
            return self._generate_real_estate_fallback_advice()

    def _generate_real_estate_fallback_advice(self) -> Dict[str, Any]:
        """Generate simple real estate advice fallback"""
        return {
            'response': """# Real Estate Advice

## Fundamentals

### Buying vs Renting

**Buying Advantages:**
- Equity building (house value goes up, paid in return)
- Stability (can stay as long as you like)
- Control (can remodel, make changes)
- Potentially lower monthly (if market is good)

**Renting Advantages:**
- Lower upfront (no down payment)
- Flexibility (can move easily)
- No maintenance costs (landlord handles repairs)
- Can invest the down payment

**When Buying Makes Sense:**
- Planning to live in the home 5+ years
- Can make a 20% down payment
- Have 6+ months of expenses saved for emergency fund
- Focus on a financially stable (some work below average)
- Plan for fixed expenses (beyond average) for startup

**When Renting makes Sense:**
- Plan to move within 2-5 years
- Can't make a down payment
- Don't have 6+ months saved
- Don't want the responsibility of repairs

### Mortgage Types Guide

**30-Year Fixed Rate:**
- Standard choice, predictable
- Lower monthly payment vs 15-year
- More interest paid over time
- Interest rate may be higher than 15-year

**15-Year Fixed Rate:**
- Higher monthly payment
- Pay off in 15 years, save thousands
- Lower interest rate than 30-year loan
- More home for equity building
- Faster equity build, lower monthly payments (but need to check your monthly payments)

### Investment Property Evaluation

**Single Family Home:**
- Easiest to rent for beginners
- High demand
- More flexible for property management
- Best for most investors starting out

**Multifamily Property:**
- Multiple rental units in one building
- Higher cash flow
- Lower vacancy risk
- Needs property management experience

**Commercial Property:**
- Offices, retail, warehousing
- Longer lease terms
- Higher income potential
- More complex to manage

### Location Selection Criteria

**Avoid:**
- **Areas with:**
- **Neighborhoods with**

**Prioritize:**
- **Consider:**

### Investment Timing

**Prepare Before Buying:**
1. **Save**
2. **Get pre-approved with**
3. **Check your**

**Market Research:**
- Check market conditions before buying
- Avoid buying at market highs
- Look for properties with potential
- Consider the area and building

### Common Real Estate Mistakes
- Buying without doing due diligence
- Stretching your budget too much
- Overlooking hidden costs
- Choosing the wrong property
- Not getting a proper inspection

**Safety Warning:** Real estate is complex and involves significant financial commitment. Always do thorough research, consult professionals, and understand all terms.

VittaAI provides this information for educational purposes. Always consider seeking professional financial advice for real estate decisions.""",
            'confidence': 0.60,
            'suggestions': [
                "Compare buying vs renting based on your long-term plans",
                "Build an emergency fund before facing a big purchase",
                "Get pre-approved for a mortgage if you're buying",
                "Save for a minimum 10% down payment, ideally 20%",
                "Research neighborhoods thoroughly before making offers",
                "Calculate all closing costs, not just down payment",
                "Consider your timeline - buying requires commitment",
                "Get a professional home inspection before your offer",
                "Don't stretch to the maximum you qualify for",
                "Factor in ongoing maintenance costs as a homeowner"
            ]
        }

    def _generate_general_financial_advice(self, query: str, language: str) -> Dict[str, Any]:
        """Generate general financial Q&A"""
        
        general_prompt = f"""You are VittaAI's expert Financial Assistant providing general financial advice.

        User query: "{query}"

        Provide comprehensive general financial advice covering:
        1. Current financial situation assessment
        2. Personalized financial guidance
        3. Methods to gather more information
        4. Effective communication strategies
        5. Investment suspectleness and insights
        6. Financial Q&A capabilities
        7. Key financial metrics to track
        8. Common financial questions answered
        9. Personalized advice generation

        Format your response in {language} with clear, actionable financial guidance.""".replace('""', query.replace('"', '\\"'))

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial advisor helping users navigate financial decisions. Respond clearly and provide practical advice for their financial situation."
                    },
                    {
                        "role": "user",
                        "content": general_prompt
                    }
                ],
                temperature=0.4,
                max_completion_tokens=2000,
                top_p=0.95,
                reasoning_effort="default",
                stream=False
            )
            
            return {
                'response': completion.choices[0].message.content or "Unable to generate financial advice. Please try again later.",
                'confidence': 0.80,
                'suggestions': [
                    "Start by organizing your current financial situation",
                    "Track all income and expenses regularly",
                    "Build an emergency fund with 3-6 months of expenses",
                    "Consider reviewing credit reports for accuracy",
                    "Plan for both current needs and future goals"
                ]
            }
            
        except Exception as e:
            return {
                'response': "Unable to generate detailed financial advice. Please request a specific topic like budget planning, credit management, retirement planning, investment guidance, or loan considerations for targeted advice.",
                'confidence': 0.65,
                'suggestions': [
                    "Try asking about specific financial topics like budgeting, credit scores, retirement planning, investments, or loans",
                    "Provide more details about your current financial situation for personalized advice",
                    "Check your free credit reports regularly for accuracy"
                ]
            }

    def qa_system(self, query: str, language: str = "en") -> Dict[str, Any]:
        """
        Question and answer system for financial queries
        
        Args:
            query: User's financial question
            language: Language for response
            
        Returns:
            Response dictionary with Q&A answer
        """
        return self._generate_general_financial_advice(query, language)

    def _build_financial_knowledge_base(self) -> dict:
        """Build default financial knowledge base"""
        return {
            'budgeting': "Budgeting fundamentals and best practices",
            'retirement': "Retirement planning and savings strategies",
            'credit': "Credit management and score improvement",
            'taxes': "Tax planning and deductions",
            'investments': "Investment strategies and portfolio management",
            'insurance': "Insurance coverage planning",
            'loans': "Loan selection and management"
        }

    def detect_financial_topic(self, query: str) -> str:
        """
        Detect the main financial topic in a query
        
        Args:
            query: User's query
            
        Returns:
            Main financial topic string
        """
        query_lower = query.lower()
        
        topics = {
            'budget': ['budget', 'spending', 'expenses', 'saving', 'financial planning'],
            'retirement': ['retirement', 'saving for retirement', 'pension', 'retire early'],
            'credit': ['credit score', 'credit score', 'credit repair', 'credit history', 'collection', 'credit card'],
            'tax': ['tax', 'taxes', 'tax planning', 'tax deductions', 'tax bracket', 'tax implication'],
            'insurance': ['insurance', 'insurance coverage', 'health insurance', 'life insurance', 'auto insurance', 'home insurance'],
            'loan': ['loan', 'mortgage', 'car loan', 'interest rate', 'loan payment', 'refinance'],
            'crypto': ['bitcoin', 'crypto', 'cryptocurrency', 'bitcoin', 'cryptos'],
            'investment': ['investment', 'invest', 'stock market', 'portfolio', 'market timing', 'investment strategy'],
            'debt': ['debt', 'debt free', 'debt consolidation', 'collection', 'budget management'],
            'realestate': ['real estate', 'property', 'home buying', 'mortgage', 'house']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in query_lower for keyword in keywords):
                return topic
                
        return 'general'