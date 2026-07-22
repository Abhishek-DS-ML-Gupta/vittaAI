"""
VittaAI - Financial AI Platform
Combines investment advice, financial assistance, and risk analysis with modern AI
"""

from .main import VittaAI
from .localization import LocalizationManager
from .investment_advisor import InvestmentAdvisor
from .financial_assistant import FinancialAssistant
from .risk_analyzer import RiskAnalyzer

__version__ = "1.0.0"
__author__ = "VittaAI Team"

__all__ = [
    "VittaAI",
    "LocalizationManager", 
    "InvestmentAdvisor",
    "FinancialAssistant", 
    "RiskAnalyzer"
]