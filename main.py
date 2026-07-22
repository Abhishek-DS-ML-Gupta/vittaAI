"""
VittaAI - Modern Financial AI Platform
Combines investment advice, financial assistance, and risk analysis
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional, List, Dict, Any
from groq import Groq
from decimal import Decimal
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

# Import modules
try:
    from investment_advisor import InvestmentAdvisor
    from financial_assistant import FinancialAssistant
    from risk_analyzer import RiskAnalyzer
    from localization import LocalizationManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative imports...")
    try:
        import importlib
        investment_advisor = importlib.import_module('investment_advisor')
        InvestmentAdvisor = investment_advisor.InvestmentAdvisor
        financial_assistant = importlib.import_module('financial_assistant')
        FinancialAssistant = financial_assistant.FinancialAssistant
        risk_analyzer = importlib.import_module('risk_analyzer')
        RiskAnalyzer = risk_analyzer.RiskAnalyzer
        localization = importlib.import_module('localization')
        LocalizationManager = localization.LocalizationManager
    except Exception as e2:
        print(f"Alternative import also failed: {e2}")
        print("This is expected if script is run directly without proper module setup")
        InvestmentAdvisor = None
        FinancialAssistant = None
        RiskAnalyzer = None
        LocalizationManager = None

class DataVisualizer:
    def __init__(self, client=None):
        self.client = client
        
    def create_visualization(self, query: str, language: str = "en") -> dict:
        return {
            'response': "Data visualization feature is currently under development.",
            'type': "visualization",
            'confidence': 1.0,
            'suggestions': []
        }

    def generate_flow_diagram(self, query: str, language: str = "en") -> str:
        if not self.client:
            return "```mermaid\ngraph TD\n    A[Error] --> B[No API Client]\n```"
            
        system_prompt = "You are a financial advisor. Create a Mermaid flowchart (graph TD) that outlines a step-by-step financial plan based on the user's query. Output ONLY the raw mermaid code wrapped in ```mermaid ... ``` codeblocks, without any other text or explanation."
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}\nLanguage: {language}"}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            content = response.choices[0].message.content.strip()
            if "```mermaid" not in content and "```" in content:
                content = content.replace("```", "```mermaid\n", 1)
            elif "```" not in content:
                content = f"```mermaid\n{content}\n```"
            return content
        except Exception as e:
            err = str(e).replace(' ', '_').replace('"', '').replace("'", "")
            return f"```mermaid\ngraph TD\n    A[Error] --> B[{err}]\n```"



class VittaAI:
    def __init__(self):
        """Initialize VittaAI with Groq API integration"""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=self.api_key)
        self.localization = LocalizationManager()
        self.advisor = InvestmentAdvisor(self.client, self.localization)
        self.assistant = FinancialAssistant(self.client, self.localization)
        self.analyzer = RiskAnalyzer(self.client, self.localization)
        self.visualizer = DataVisualizer(self.client)

    def generate_response(self, query: str, language: str = "en", 
                         verbose: bool = False) -> Dict[str, Any]:
        """Generate intelligent financial response based on query analysis"""
        query_lower = query.lower()
        response = {
            'response': "",
            'type': "general",
            'confidence': 0.0,
            'suggestions': []
        }

        # Analyze query intent
        if any(keyword in query_lower for keyword in ['invest', 'stock', 'portfolio', 'buy', 'sell', 'recommend']):
            response.update(self.advisor.get_investment_recommendation(query, language))
        elif any(keyword in query_lower for keyword in ['budget', 'save', 'expense', 'spend', 'finance']):
            response.update(self.assistant.get_financial_advice(query, language))
        elif any(keyword in query_lower for keyword in ['risk', 'analyze', 'analysis', 'danger', 'dangerous']):
            response.update(self.analyzer.analyze_risk(query, language))
        elif any(keyword in query_lower for keyword in ['chart', 'graph', 'plot', 'visual']):
            response.update(self.visualizer.create_visualization(query, language))
        elif any(keyword in query_lower for keyword in ['hello', 'hi', 'hey']):
            response['response'] = self.localization.t("greeting", language)
            response['confidence'] = 1.0
        else:
            # General Q&A with financial knowledge
            response.update(self.assistant.qa_system(query, language))

        if verbose:
            print(f"Query: {query}")
            print(f"Response Type: {response['type']}")
            print(f"Confidence: {response['confidence']}")
            print(f"Suggestions: {response.get('suggestions', [])}")

        return response

    def generate_flow_diagram(self, query: str, language: str = "en") -> str:
        """Generate a Mermaid flow diagram for the financial plan."""
        return self.visualizer.generate_flow_diagram(query, language)

    def streaming_response(self, query: str, language: str = "en", 
                          verbose: bool = False) -> str:
        """Generate streaming response for chat interface"""
        response_data = self.generate_response(query, language, verbose)
        return response_data['response']

    def get_supported_languages(self) -> List[str]:
        """Return list of supported languages"""
        return self.localization.get_supported_languages()

    def get_available_services(self) -> Dict[str, Dict]:
        """Return description of available services"""
        return {
            'investment_advisor': {
                'description': 'Get personalized investment recommendations and portfolio guidance',
                'capabilities': ['stock analysis', 'portfolio optimization', 'market trends', 'risk assessment']
            },
            'financial_assistant': {
                'description': 'Personal financial planning and budgeting assistance',
                'capabilities': ['budget planning', 'expense tracking', 'savings goals', 'financial Q&A']
            },
            'risk_analyzer': {
                'description': 'Comprehensive risk analysis for financial decisions',
                'capabilities': ['market risk analysis', 'portfolio risk assessment', 'economic indicators', 'scenario analysis']
            },
            'data_viz': {
                'description': 'Interactive data visualization and market charts',
                'capabilities': ['price charts', 'performance graphs', 'correlation analysis', 'portfolio visualization']
            }
        }


if __name__ == "__main__":
    # Test the system
    vitta_ai = VittaAI()
    
    print("VittaAI initialized successfully!")
    print("Available services:", list(vitta_ai.get_available_services().keys()))
    print("Supported languages:", vitta_ai.get_supported_languages())
    
    # Test response
    test_query = "What should I invest in?"
    response = vitta_ai.generate_response(test_query, "en", verbose=True)
    print("\nTest Response:")
    print(response['response'])