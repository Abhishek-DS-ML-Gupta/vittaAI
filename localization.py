"""
VittaAI - Localization Manager
Provides multi-language support for financial content
"""

from typing import Dict, Any, List


class LocalizationManager:
    def __init__(self):
        """Initialize localization manager with default English content"""
        self.supported_languages = {
            'en': ('English', '🇺🇸', {}),
            'es': ('Spanish', '🇪🇸', self._get_spanish_content()),
            'hi': ('Hindi', '🇮🇳', self._get_hindi_content()),
            'fr': ('French', '🇫🇷', self._get_french_content()),
            'de': ('German', '🇩🇪', self._get_german_content()),
            'ja': ('Japanese', '🇯🇵', self._get_japanese_content())
        }

    def get_supported_languages(self) -> Dict[str, List[str]]:
        """Get list of supported languages with details"""
        return {k: [info[0], info[1]] for k, info in self.supported_languages.items()}

    def t(self, key: str, language: str = "en") -> str:
        """
        Get translated text for a given key
        
        Args:
            key: Translation key 
            language: Language code
            
        Returns:
            Translated text
        """
        # English is default
        if language.lower() not in self.supported_languages:
            return self.supported_languages.get('en', ('English', '🇺🇸', {}))[2].get(key, key)
        
        # Get content in target language
        translations = self.supported_languages[language.lower()][2]
        return translations.get(key, key)

    def _get_default_content(self) -> Dict[str, str]:
        """Get default English content"""
        return {
            # Greeting and welcome
            'greeting': "Hello! I'm VittaAI, your intelligent financial intelligence platform. How can I help you today with your financial decisions?",
            'welcome': "welcome",
            'financial_journey': "Start Your Financial Journey",
            
            # Service descriptions
            'investment_advisor': "Personalized investment recommendations, portfolio optimization, market trends",
            'financial_assistant': "Budget planning, expense tracking, savings goals, financial Q&A",
            'risk_analyzer': "Comprehensive risk assessment, portfolio risk analysis, economic indicators",
            'data_viz': "Interactive charts, performance graphs, portfolio visualization",
            
            # UI elements
            'analyze_insights': "Analyse & Get Insights",
            'language': "Language",
            'your_financial_question': "Your Financial Question",
            'portfolio_analysis': "Portfolio Analysis",
            'risk_analysis': "Risk Analysis",
            'supported_services': "Supported Services",
            
            # Funding suggestions
            'strategic_recommendations': "Strategic Recommendations",
            'actionable_suggestions': "Actionable Suggestions",
            'risk_management_strategies': "Risk Management Strategies",
            
            # Portfolio analysis
            'portfolio_type': "Portfolio Type",
            'confidence': "Confidence",
            'portfolio_optimization_suggestions': "Portfolio Optimization Suggestions",
            
            # Risk analysis
            'risk_assessment': "Risk Assessment",
            'risk_level': "Risk Level",
            
            # Quick navigation
            'budgeting': "Budgeting",
            'retirement': "Retirement",
            'credit': "Credit",
            'investing': "Investing",
            'loan': "Loans",
            
            # Section headers
            'investment_recommendations': "Investment Recommendations",
            'risk_analysis_header': "Risk Assessment",
            'financial_analysis': "Financial Analysis",
            
            # Footer
            'powered_by': "Powered by Groq AI with Qwen 3.6 Model",
            'modern_responsive': "Modern, Responsive, Intelligent",
            'multi_language': "Multi-language support • Real-time responses • Comprehensive analysis"
        }

    def _get_spanish_content(self) -> Dict[str, str]:
        """Get Spanish translations"""
        return {
            'greeting': "¡Hola! Soy VittaAI, su plataforma inteligente de inteligencia financiera. ¿Cómo puedo ayudarlo hoy con sus decisiones financieras?",
            'welcome': "Bienvenido",
            'financial_journey': "Comience su Viaje Financiero",
            'investment_advisor': "Recomendaciones de inversión personalizadas, optimización de cartera, tendencias de mercado",
            'financial_assistant': "Planificación presupuestaria, seguimiento de gastos, objetivos de ahorro, preguntas financieras",
            'risk_analyzer': "Evaluación de riesgos integral, análisis de riesgo de cartera, indicadores económicos",
            'data_viz': "Gráficos interactivos, gráficos de rendimiento, visualización de cartera",
            'analyze_insights': "Analizar y Obtener Insights",
            'language': "Idioma",
            'your_financial_question': "Su Pregunta Financiera",
            'portfolio_analysis': "Análisis de Cartera",
            'risk_analysis': "Análisis de Riesgo",
            'supported_services': "Servicios Soportados",
            'strategic_recommendations': "Recomendaciones Estratégicas",
            'actionable_suggestions': "Sugerencias Accionables",
            'portfolio_type': "Tipo de Cartera",
            'risk_assessment': "Evaluación de Riesgos",
            'budgeting': "Presupuestación",
            'retirement': "Retiro",
            'credit': "Crédito",
            'investing': "Inversión",
            'loan': "Préstamos",
            'investment_recommendations': "Recomendaciones de Inversión",
            'risk_analysis_header': "Evaluación de Riesgos",
            'financial_analysis': "Análisis Financiero"
        }

    def _get_hindi_content(self) -> Dict[str, str]:
        """Get Hindi translations"""
        return {
            'greeting': "नमस्ते! मैं VittaAI हूं, आपका बुद्धिमान वित्तीय बुद्धि प्लेटफ़ॉर्म। मैं आज आपके वित्तीय निर्णयों में आपकी कैसे मदद कर सकता हूं?",
            'welcome': "स्वागत है",
            'financial_journey': "अपनी वित्तीय यात्रा शुरू करें",
            'investment_advisor': "व्यक्तिगत निवेश सुझाव, पोर्टफोलियो अनुकूलन, बाजार रुझान",
            'financial_assistant': "बजट योजना, खर्च ट्रैकिंग, बचत लक्ष्य, वित्तीय प्रश्नोत्तर",
            'risk_analyzer': "पूर्ण जोखिम मूल्यांकन, पोर्टफोलियो जोखिम विश्लेषण, आर्थिक संकेतक",
            'data_viz': "इंटरैक्टिव चार्ट, प्रदर्शन ग्राफ़, पोर्टफोलियो विज़ुअलाइज़ेशन",
            'analyze_insights': "विश्लेषण करें और समाधान प्राप्त करें",
            'language': "भाषा",
            'your_financial_question': "आपका वित्तीय प्रश्न",
            'portfolio_analysis': "पोर्टफोलियो विश्लेषण",
            'risk_analysis': "जोखिम विश्लेषण",
            'supported_services': "समर्थित सेवाएं",
            'strategic_recommendations': "रणनीतिक सुझाव",
            'actionable_suggestions': "कार्यात्मक सुझाव",
            'portfolio_type': "पोर्टफोलियो प्रकार",
            'risk_assessment': "जोखिम मूल्यांकन",
            'budgeting': "जल प्रबंधन",
            'retirement': "पेंशन",
            'credit': "Credit",
            'investing': "निवेश",
            'loan': "ऋण",
            'investment_recommendations': "निवेश सुझाव",
            'risk_analysis_header': "जोखिम समाधान",
            'financial_analysis': "वित्तीय विश्लेषण"
        }

    def _get_french_content(self) -> Dict[str, str]:
        """Get French translations"""
        return {
            'greeting': "Bonjour ! Je suis VittaAI, votre plateforme intelligente d'intelligence financière. Comment puis-je vous aider aujourd'hui avec vos décisions financières ?",
            'welcome': "Bienvenue",
            'financial_journey': "Commencez Votre Voyage Financier",
            'investment_advisor': "Recommandations d'investissement personnalisées, optimisation de portefeuille, tendances du marché",
            'financial_assistant': "Planification budgétaire, suivi des dépenses, objectifs d'épargne, questions financières",
            'risk_analyzer': "Évaluation complète des risques, analyse des risques de portefeuille, indicateurs économiques",
            'data_viz': "Graphiques interactifs, graphiques de performance, visualisation de portefeuille",
            'analyze_insights': "Analyser et Obtention de Conseils",
            'language': "Langue",
            'your_financial_question': "Votre Question Financière",
            'portfolio_analysis': "Analyse de Portefeuille",
            'risk_analysis': "Analyse des Risques",
            'supported_services': "Services Supportés",
            'strategic_recommendations': "Recommandations Stratégiques",
            'actionable_suggestions': "Suggérences Actionnables",
            'portfolio_type': "Type de Portefeuille",
            'risk_assessment': "Évaluation des Risques",
            'budgeting': "Gestion Budgétaire",
            'retirement': "Retraite",
            'credit': "Crédit",
            'investing': "Investissement",
            'loan': "Prêts",
            'investment_recommendations': "Recommandations d'Investissement",
            'risk_analysis_header': "Évaluation des Risques",
            'financial_analysis': "Analyse Financière"
        }

    def _get_german_content(self) -> Dict[str, str]:
        """Get German translations"""
        return {
            'greeting': "Hallo! Ich bin VittaAI, Ihre intelligente Finanzintelligenz-Plattform. Wie kann ich Ihnen heute bei Ihrer Finanzentscheidung helfen?",
            'welcome': "Willkommen",
            'financial_journey': "Beginnen Sie Ihre finanzielle Reise",
            'investment_advisor': "Personalisierte Anlageberatung, Portefolienoptimierung, Markttrends",
            'financial_assistant': "Haushaltsplanung, Ausgabenverfolgung, Sparziele, Finanzfragen",
            'risk_analyzer': "Umfassende Risikobewertung, Portefolienrisikoanalyse, Wirtschaftsinformationen",
            'data_viz': "Interaktive Diagramme, Performance-Graphen, Portefolienvisualisierung",
            'analyze_insights': "Analyse und Erhalt von Einblicken",
            'language': "Sprache",
            'your_financial_question': "Ihre Finanzfrage",
            'portfolio_analysis': "Portfolianalyse",
            'risk_analysis': "Risikoanalyse",
            'supported_services': "Unterstützte Services",
            'strategic_recommendations': "Strategische Empfehlungen",
            'actionable_suggestions': "Handlungsorientierte Vorschläge",
            'portfolio_type': "Portfolio-Typ",
            'risk_assessment': "Risikobewertung",
            'budgeting': "Haushaltsführung",
            'retirement': "Rente",
            'credit': "Kredit",
            'investing': "Investition",
            'loan': "Kredite",
            'investment_recommendations': "Anlageempfehlungen",
            'risk_analysis_header': "Risikobewertung",
            'financial_analysis': "Finanzanalyse"
        }

    def _get_japanese_content(self) -> Dict[str, str]:
        """Get Japanese translations"""
        return {
            'greeting': "こんにちは！私はVittaAI、あなたの賢明な金融インテリジェンスプラットフォームです。今日、金銭的にどのように助けられるか教えてください。",
            'welcome': "ようこそ",
            'financial_journey': "金融への旅を始める",
            'investment_advisor': "個人投資勧告、ポートフォリオ最適化、市場トレンド",
            'financial_assistant': "予算計画、支出追跡、貯金目標、 finance ",
            'risk_analyzer': "リスク評価、ポートフォリオ分析、経済指標",
            'data_viz': "インタラクティブチャート、パフォーマンスグラフ、ポートフォリオ可視化",
            'analyze_insights': "分析して洞察を取得",
            'language': "言語にする",
            'your_financial_question': "あなたのfinance ",
            'portfolio_analysis': "ポートフォリオ分析",
            'risk_analysis': "リスク分析",
            'supported_services': "サポートされているサービス",
            'strategic_recommendations': "戦略的な推奨事項",
            'actionable_suggestions': "実行可能な提案",
            'portfolio_type': "ポートフォリオタイプ",
            'risk_assessment': "リスク評価",
            'budgeting': "予算管理",
            'retirement': "年金",
            'credit': "クレジット",
            'investing': "投資",
            'loan': "貸し出し",
            'investment_recommendations': "投資勧告",
            'risk_analysis_header': "リスク評価",
            'financial_analysis': "financial "
        }

    def update_aiai(self, key: str, translations: Dict[str, str], language: str = "en"):
        """
        Update AI prompts with localized content
        
        Args:
            key: AI analysis key
            translations: Dictionary of localized translations
            language: Target language
        """
        # Store in registry (would need persistent storage in real app)
        language_code = language.lower().split()[0]
        if language_code in self.supported_languages:
            # Add to existing translations
            current_translations = self.supported_languages[language_code][2]
            current_translations.update(translations)
            self.supported_languages[language_code] = (
                self.supported_languages[language_code][0],
                self.supported_languages[language_code][1],
                current_translations
            )

    def get_language_content(self, language: str) -> Dict[str, Any]:
        """
        Get all content for a specific language
        
        Args:
            language: Language code
            
        Returns:
            Dictionary containing language info and translations
        """
        language_lower = language.lower().split()[0]
        if language_lower not in self.supported_languages:
            return None
            
        return {
            'language': self.supported_languages[language_lower][0],
            'flag': self.supported_languages[language_lower][1],
            'translations': self.supported_languages[language_lower][2]
        }