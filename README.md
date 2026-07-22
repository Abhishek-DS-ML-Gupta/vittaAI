# VittaAI - Financial Intelligence Platform

VittaAI is a modern, responsive, and intelligent financial intelligence platform built with Python, Gradio, and Groq API. It acts as your personal financial advisor and risk analyzer.

## Features
- **Intelligent Financial Advisor**: Ask questions about budgeting, investments, and general financial planning.
- **Risk Assessment**: Analyze the risks in your financial decisions or portfolio.
- **Flow Diagrams**: Generate visual step-by-step Mermaid flowchart diagrams for your financial plans.
- **Multilingual Support**: Supports English, Spanish, Hindi, French, German, and Japanese.

## Setup
1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Groq API key as an environment variable (or put it in a `.env` file):
   ```bash
   export GROQ_API_KEY="your-api-key"
   ```
   *(Note: The application falls back to a default key if not provided, but it's recommended to use your own.)*

## Usage
Run the main Gradio application:
```bash
python app.py
```
Then navigate to `http://127.0.0.1:7860` in your web browser.
