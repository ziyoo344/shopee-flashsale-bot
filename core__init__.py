"""
Shopee Flash Sale Bot Core Module
"""

from .browser import BrowserManager
from .auth import AuthManager
from .order import OrderManager
from .utils import Utils

__all__ = ['BrowserManager', 'AuthManager', 'OrderManager', 'Utils']