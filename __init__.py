"""
Facebook Bot Package

This package provides functionality for automating Facebook interactions
including login, cookie management, and basic navigation.

Main components:
- config.py: Configuration settings and credentials
- functions.py: Core functionality for login and cookie management

Usage:
    from functions import initialize_driver, navigate_to_facebook, is_logged_in
    from functions import load_cookies, save_cookies, login_with_credentials
    from config import *
"""

__version__ = "1.0.0"
__author__ = "Facebook Bot"
__description__ = "Facebook automation bot for login and basic interactions"

# Import main functions for easy access
from .functions import (
    initialize_driver,
    navigate_to_facebook,
    is_logged_in,
    load_cookies,
    save_cookies,
    login_with_credentials,
    get_chrome_options
)

from .config import (
    FB_EMAIL,
    FB_PASSWORD,
    COOKIES_FILE,
    DEBUG
)

__all__ = [
    'initialize_driver',
    'navigate_to_facebook', 
    'is_logged_in',
    'load_cookies',
    'save_cookies',
    'login_with_credentials',
    'get_chrome_options',
    'FB_EMAIL',
    'FB_PASSWORD',
    'COOKIES_FILE',
    'DEBUG'
]