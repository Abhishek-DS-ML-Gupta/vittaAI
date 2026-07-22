"""
VittaAI - Modern Financial AI Application
Main Gradio Interface with Streaming Responses
"""

import gradio as gr
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import VittaAI
from localization import LocalizationManager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)