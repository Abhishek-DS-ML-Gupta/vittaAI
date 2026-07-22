"""
VittaAI - Modern Financial AI Application
Main Gradio Interface
"""

import gradio as gr
import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import VittaAI
from localization import LocalizationManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VittaAIGradioApp:
    def __init__(self):
        """Initialize VittaAI with Gradio interface"""
        self.ai = VittaAI()
        self.supported_languages = self.ai.get_supported_languages()
        
        # Create Gradio app
        self.theme = gr.themes.Soft()
        self.css = """
        .app-container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .ai-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 16px; color: white; text-align: center; margin-bottom: 30px; }
        .ai-header h1 { font-size: 3em; margin: 0; font-weight: 700; }
        .main-chat { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    border-radius: 16px; padding: 25px; min-height: 600px; }
        .panel { background: white; border-radius: 16px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        """
        self.demo = gr.Blocks(
            title="VittaAI - Financial Intelligence Platform"
        )
        
        self.setup_gradio()

    def setup_gradio(self):
        """Setup and configure the Gradio interface"""
        
        with self.demo:
            # Main AI Header
            gr.Markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&display=swap');
            </style>
            """)
            
            gr.Markdown("""
            <div class="ai-header">
                <h1>🪙 VittaAI</h1>
                <p>⭐ Intelligent Financial Intelligence Platform</p>
                <p>🚀 Your Personal Financial Advisor & Risk Analyzer</p>
            </div>
            """)
            
            gr.Markdown("""
            ## Welcome to VittaAI
            Start Your Financial Journey
            """)
            
            # Main Chat Interface
            with gr.Column():
                language_select = gr.Dropdown(
                    choices=["English", "Spanish", "Hindi", "French", "German", "Japanese"],
                    value="English",
                    label="🌐 Language",
                    show_label=True
                )
                
                query_input = gr.Textbox(
                    label="💭 Your Financial Question",
                    placeholder="Type your financial question here... (e.g., I'm a conservative investor looking for safe recommendations)",
                    lines=3
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🔍 Analyze & Get Insights", variant="primary", size="lg")
                    flow_btn = gr.Button("📊 Generate Flow Diagram", variant="secondary", size="lg")
                
                result_output = gr.HTML(label="📊 AI Response")
                suggestion_output = gr.Markdown(label="💡 Actionable Suggestions")
                flow_diagram_output = gr.Markdown(label="📈 Financial Plan Flow Diagram")
            
            # Examples
            gr.Markdown("""
            ### Example Questions
            1. "I'm a conservative investor looking for safe recommendations"
            2. "What should I do for retirement planning?"
            3. "How can I improve my credit score?"
            4. "Analyze my credit risk factors"
            5. "What percentage should I allocate to tech stocks?"
            6. "How do I reduce my debt?"
            7. "What's the best way to invest for beginners?"
            8. "Analyze my portfolio risk: AAPL 30%, GOOGL 20%, TSLA 50%"
            """)
            
            # Event handlers
            inputs = [query_input, language_select]
            
            submit_btn.click(
                self.process_query,
                inputs=inputs,
                outputs=[result_output, suggestion_output]
            )
            
            flow_btn.click(
                self.generate_flow,
                inputs=inputs,
                outputs=flow_diagram_output
            )
            
            # Footer
            gr.Markdown("""
            <div style="text-align: center; padding: 20px; margin-top: 40px;">
                <p>🚀 VittaAI - Powered by Groq AI with Qwen 3.6 Model</p>
                <p>⭐ Modern, Responsive, Intelligent Financial Intelligence</p>
                <p>🌐 Multi-language support • 💬 Real-time streaming responses • 📊 Comprehensive analysis</p>
            </div>
            """)

    def process_query(self, query: str, language: str):
        """Process user query and generate comprehensive response"""
        
        if not query.strip():
            yield """
            <div class="panel">
                <h2>✨ Welcome to VittaAI</h2>
                <p>I'm here to help you make smart financial decisions.</p>
                <p>Try asking about:</p>
                <ul>
                    <li>💡 Investment guidance and portfolio analysis</li>
                    <li>💰 Budget planning and financial planning</li>
                    <li>📈 Retirement and savings strategies</li>
                    <li>🏦 Credit scores and financial health</li>
                    <li>⚡ Risk assessment and investment safety</li>
                    <li>🔔 Loan options and financial management</li>
                    <li>🔐 Financial Q&A and analysis</li>
                </ul>
            </div>
            """, ""
            return
        
        try:
            language_code = language.lower().split()[0]
            response_data = self.ai.generate_response(query, language_code, verbose=True)
            
            result_html = self._format_response(query, response_data, language)
            
            suggestions_str = "\n".join(f"- {s}" for s in response_data.get('suggestions', []))
            final_suggestions = f"### 💡 Actionable Suggestions\n{suggestions_str}"
            
            # Tipper animation (typewriter effect)
            chunk_size = 20
            for i in range(0, len(result_html), chunk_size):
                yield result_html[:i+chunk_size], final_suggestions
                time.sleep(0.01)
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            yield f"""
            <div class="panel" style="border-color: red;">
                <h2 style="color: red;">⚠️ Error</h2>
                <p>Please try again later. Error: {str(e)}</p>
            </div>
            """, "Unable to generate suggestions at this time."

    def generate_flow(self, query: str, language: str):
        """Generate flowchart based on user query"""
        if not query.strip():
            return "Please enter a financial scenario to generate a flow diagram."
        try:
            language_code = language.lower().split()[0]
            mermaid_code = self.ai.generate_flow_diagram(query, language_code)
            return mermaid_code
        except Exception as e:
            logger.error(f"Error generating flow diagram: {e}")
            return f"```mermaid\ngraph TD\n    A[Error] --> B[{str(e).replace(' ', '_')}]\n```"

    def process_portfolio(self, portfolio_str: str, language: str):
        """Process portfolio analysis request"""
        
        if not portfolio_str.strip():
            return """
            <div class="panel">
                <h2>📊 Portfolio Analysis</h2>
                <p>Please enter your portfolio allocation format:</p>
                <p>Example: AAPL 20%, GOOGL 30%, TSLA 50%</p>
            </div>
            """
        
        try:
            language_code = language.lower().split()[0]
            response_data = self.ai.portfolio_risk_assessment(portfolio_str, language_code)
            
            result_html = self._format_portfolio_response(response_data)
            
            return result_html
            
        except Exception as e:
            logger.error(f"Error processing portfolio: {e}")
            return f"""
            <div class="panel" style="border-color: red;">
                <h2 style="color: red;">⚠️ Error in Portfolio Analysis</h2>
                <p>Please enter portfolio in format like: AAPL 20%, GOOGL 30%, TSLA 50%</p>
                <p>Error: {str(e)}</p>
            </div>
            """

    def process_risk(self, query: str, language: str):
        """Process risk analysis request"""
        
        if not query.strip():
            return """
            <div class="panel">
                <h2>⚡ Risk Assessment</h2>
                <p>Describe your investment situation or risk concerns to get analysis.</p>
                <p>Example: "I'm worried about market risk" or "Analyze my portfolio risk"</p>
            </div>
            """
        
        try:
            language_code = language.lower().split()[0]
            response_data = self.ai.analyze_risk_factors(query, language_code)
            
            result_html = self._format_risk_response(response_data)
            
            return result_html
            
        except Exception as e:
            logger.error(f"Error processing risk: {e}")
            return f"""
            <div class="panel" style="border-color: red;">
                <h2 style="color: red;">⚠️ Error in Risk Analysis</h2>
                <p>Error: {str(e)}</p>
            </div>
            """

    def _format_response(self, query: str, response_dict, language: str) -> str:
        """Format and customize response based on content type"""
        
        response_type = response_dict.get('type', 'general')
        response_text = response_dict.get('response', '')
        
        # Different response formatting based on type
        if response_type == 'investment_recommendation':
            return f"""
            <div class="panel">
                <h2>📈 Investment Recommendations</h2>
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin: 10px 0;">
                    {response_text}
                </div>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                    <h3 style="margin: 0 0 10px 0;">💡 Strategic Recommendations</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        {''.join(f'<li>{s}</li>' for s in response_dict.get('suggestions', [])[:10])}
                    </ul>
                </div>
                <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                    ⚠️ VittaAI provides this information for educational purposes. Consider seeking professional financial advice for substantial investments.
                </p>
            </div>
            """
        
        elif response_type == 'risk_analysis':
            return f"""
            <div class="panel">
                <h2>⚔️ Risk Assessment</h2>
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin: 10px 0;">
                    {response_text}
                </div>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                    <h3 style="margin: 0 0 10px 0;">🎯 Risk Management Strategies</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        {''.join(f'<li>{s}</li>' for s in response_dict.get('suggestions', [])[:10])}
                    </ul>
                </div>
                <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                    ⚠️ Risk assessments are educational. Always consider professional guidance for significant financial decisions.
                </p>
            </div>
            """
        
        else:
            return f"""
            <div class="panel">
                <h2>📊 Financial Analysis</h2>
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin: 10px 0;">
                    {response_text}
                </div>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                    <h3 style="margin: 0 0 10px 0;">💡 Actionable Suggestions</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        {''.join(f'<li>{s}</li>' for s in response_dict.get('suggestions', [])[:10])}
                    </ul>
                </div>
            </div>
            """

    def _format_portfolio_response(self, response_dict) -> str:
        """Format portfolio analysis response"""
        response_type = response_dict.get('type', 'financial_advice')
        response_text = response_dict.get('response', '')
        risk_level = response_dict.get('risk_level', 'moderate')
        confidence = response_dict.get('confidence', 0.0) * 100
        
        return f"""
        <div class="panel">
            <h2>💼 Portfolio Risk Analysis</h2>
            <p style="margin-bottom: 15px;">
                <strong>Portfolio Type:</strong> {response_type} | 
                <strong>Risk Level:</strong> {risk_level} | 
                <strong>Confidence:</strong> {confidence:.0f}%
            </p>
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin: 10px 0;">
                {response_text}
            </div>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                <h3 style="margin: 0 0 10px 0;">💡 Portfolio Optimization Suggestions</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    {''.join(f'<li>{s}</li>' for s in response_dict.get('suggestions', [])[:10])}
                </ul>
            </div>
            <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                ⚠️ Portfolio analysis is educational. Always consult a professional advisor for professional guidance.
            </p>
        </div>
        """

    def _format_risk_response(self, response_dict) -> str:
        """Format risk analysis response"""
        response_type = response_dict.get('type', 'risk_analysis')
        response_text = response_dict.get('response', '')
        risk_level = response_dict.get('risk_level', 'moderate')
        confidence = response_dict.get('confidence', 0.0) * 100
        
        return f"""
        <div class="panel">
            <h2>⚔️ Risk Assessment</h2>
            <p style="margin-bottom: 15px;">
                <strong>Risk Analysis:</strong> {response_type} | 
                <strong>Risk Level:</strong> {risk_level} | 
                <strong>Confidence:</strong> {confidence:.0f}%
            </p>
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin: 10px 0;">
                {response_text}
            </div>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 8px; margin: 10px 0; color: white;">
                <h3 style="margin: 0 0 10px 0;">🎯 Risk Management Strategies</h3>
                <ul style="margin: 0; padding-left: 20px;">
                    {''.join(f'<li>{s}</li>' for s in response_dict.get('suggestions', [])[:10])}
                </ul>
            </div>
            <p style="margin-top: 15px; font-size: 0.9em; color: #666;">
                ⚠️ Risk assessments are for education. Always seek professional advice for major financial decisions.
            </p>
        </div>
        """

    def launch(self, **kwargs):
        """Launch the Gradio app"""
        
        app_name = kwargs.pop('name', 'VittaAI')
        share = kwargs.pop('share', False)
        
        logger.info(f"Launching {app_name}...")
        
        return self.demo.launch(
            server_name="0.0.0.0",
            share=share,
            theme=self.theme,
            css=self.css,
            **kwargs
        )


def main():
    """Main application entry point"""
    print("🚀 Starting VittaAI - Financial Intelligence Platform...")
    print("📊 Initializing Groq integration with Qwen 3.6-27b model...")
    
    gradio_app = VittaAIGradioApp()
    
    print("\n✅ VittaAI is ready!")
    print("💡 Launching on local server...")
    
    gradio_app.launch(name="VittaAI", share=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error launching VittaAI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)