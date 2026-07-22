"""
VittaAI - Application Entry Point
Sets up the application with proper module resolution
"""

import sys
import os

# Add current directory to the path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import VittaAIGradioApp

def main():
    """Main application entry point"""
    print("🚀 Starting VittaAI - Financial Intelligence Platform...")
    print("📊 Initializing Groq integration with Qwen 3.6-27b model...")
    print("🌐 Loading multi-language support...")
    
    gradio_app = VittaAIGradioApp()
    
    print("\n✅ VittaAI is ready!")
    print("💡 Launching on local host...")
    
    gradio_app.launch(name="VittaAI", share=False)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error launching VittaAI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)