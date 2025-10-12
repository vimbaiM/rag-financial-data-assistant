# ============================================================================
#
# Copyright (c) 2025, Vimbai Mangwiro. All rights reserved.
# Use of this source code is governed by a BSD 3-Clause License that can be
# found in the LICENSE file.
#
# ============================================================================

"""
Enhanced URL building utilities for financial APIs
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Optional
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

class URLBuilderInterface(ABC):
    """Abstract base class for URL builders"""

    @abstractmethod
    def add_params(self, params: Dict[str, str]) -> None:
        """Add parameters to the URL"""
        raise NotImplementedError

    @abstractmethod
    def build(self) -> str:
        """Build and return the complete URL"""
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> Optional[str]:
        """Get the built URL"""
        raise NotImplementedError

class AlphaVantageURLBuilder(URLBuilderInterface):
    """URL builder for Alpha Vantage API"""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.params = self._init_params()
        self._url: Optional[str] = None

    def _init_params(self) -> Dict[str, str]:
        """Initialize with API key"""
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable not set")
        return {"apikey": api_key}

    def add_params(self, params: Dict[str, str]) -> None:
        """Add additional parameters with validation"""
        if not isinstance(params, dict):
            raise TypeError("Parameters must be a dictionary")

        # Validate required Alpha Vantage params
        if 'function' not in params:
            raise ValueError("Alpha Vantage requires 'function' parameter")

        self.params.update(params)

    def build(self) -> str:
        """Build the complete URL"""
        query_string = urlencode(self.params)
        self._url = f"{self.BASE_URL}?{query_string}"
        return self._url

    @property
    def url(self) -> Optional[str]:
        """Get the built URL"""
        return self._url

#TODO: Switch to Factory pattern
class URLDirector:
    """Director for orchestrating URL building"""

    def __init__(self, builder: URLBuilderInterface):
        self.builder = builder

    def construct_url(self, params: Dict[str, str]) -> str:
        """Construct URL using the builder"""
        self.builder.add_params(params)
        return self.builder.build()
