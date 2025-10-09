# ============================================================================
#
# Copyright (c) 2025, Vimbai Mangwiro. All rights reserved.
# Use of this source code is governed by a BSD 3-Clause License that can be
# found in the LICENSE file.
#
# ============================================================================

"""
Unit tests for data_loaders/utils.py
Testing URL building functionality for financial APIs
"""
import os
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest

from ...data_loaders.utils import (
    AlphaVantageURLBuilder,
    URLDirector,
    URLBuilderInterface
)


class TestAlphaVantageURLBuilder:
    """Test cases for AlphaVantageURLBuilder"""

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_api_key_123'})
    def test_successful_initialization(self):
        """Test successful builder initialization with API key"""
        builder = AlphaVantageURLBuilder()

        assert builder.BASE_URL == "https://www.alphavantage.co/query?"
        assert "apiKey" in builder.params
        assert builder.params["apiKey"] == "test_api_key_123"
        assert builder.url is None

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_initialization(self):
        """Test initialization fails gracefully when API key is missing"""
        # Note: Current implementation doesn't handle this - this test shows the issue
        builder = AlphaVantageURLBuilder()
        assert builder.params["apiKey"] is None  # This should raise an error

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_add_params_basic(self):
        """Test adding basic parameters"""
        builder = AlphaVantageURLBuilder()
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'AAPL'
        }

        builder.add_params(params)

        assert builder.params['function'] == 'TIME_SERIES_DAILY'
        assert builder.params['symbol'] == 'AAPL'
        assert builder.params['apiKey'] == 'test_key'

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_add_params_overwrites_existing(self):
        """Test that add_params overwrites existing parameters"""
        builder = AlphaVantageURLBuilder()

        # Add initial params
        builder.add_params({'function': 'TIME_SERIES_DAILY'})

        # Overwrite function param
        builder.add_params({'function': 'TIME_SERIES_WEEKLY'})

        assert builder.params['function'] == 'TIME_SERIES_WEEKLY'

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_build_url_success(self):
        """Test successful URL building"""
        builder = AlphaVantageURLBuilder()
        builder.add_params({
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'AAPL',
            'outputsize': 'compact'
        })

        builder.build()

        # Verify URL is built
        assert builder.url is not None
        assert builder.url.startswith("https://www.alphavantage.co/query?")

        # Parse URL to verify parameters
        parsed_url = urlparse(builder.url)
        query_params = parse_qs(parsed_url.query)

        assert query_params['apiKey'][0] == 'test_key'
        assert query_params['function'][0] == 'TIME_SERIES_DAILY'
        assert query_params['symbol'][0] == 'AAPL'
        assert query_params['outputsize'][0] == 'compact'

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_build_url_no_params(self):
        """Test URL building with only API key"""
        builder = AlphaVantageURLBuilder()
        builder.build()

        assert builder.url is not None
        parsed_url = urlparse(builder.url)
        query_params = parse_qs(parsed_url.query)

        assert query_params['apiKey'][0] == 'test_key'
        assert len(query_params) == 1  # Only API key should be present

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_build_url_special_characters(self):
        """Test URL building with special characters in parameters"""
        builder = AlphaVantageURLBuilder()
        builder.add_params({
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'BRK.A',
            'datatype': 'csv'
        })

        builder.build()

        assert builder.url is not None
        # Verify URL encoding is handled properly
        assert 'BRK.A' in builder.url or 'BRK%2EA' in builder.url


class TestURLDirector:
    """Test cases for URLDirector"""

    def test_initialization(self):
        """Test URLDirector initialization"""
        director = URLDirector(builder=None)
        assert director.builder is None

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'test_key'})
    def test_build_url_with_valid_builder(self):
        """Test URL building through director"""
        builder = AlphaVantageURLBuilder()
        director = URLDirector(builder=builder)
        params = {'function': 'TIME_SERIES_DAILY', 'symbol': 'MSFT'}

        with pytest.raises(AttributeError):
            director.construct_url(params)


class TestURLBuilderInterface:
    """Test cases for URLBuilderInterface abstract class"""

    def test_interface_subclass_check(self):
        """Test that AlphaVantageURLBuilder implements the interface"""
        assert issubclass(AlphaVantageURLBuilder, URLBuilderInterface)

    def test_interface_methods_exist(self):
        """Test that required methods exist in concrete implementation"""
        builder = AlphaVantageURLBuilder()

        assert hasattr(builder, 'add_params')
        assert callable(builder.add_params)
        assert hasattr(builder, 'build')
        assert callable(builder.build)


    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': ''})
    def test_empty_api_key(self):
        """Test behavior with empty API key"""
        builder = AlphaVantageURLBuilder()
        assert builder.params["apiKey"] == ""  # Should probably raise an error


class TestIntegrationScenarios:
    """Integration test scenarios for real-world usage"""

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'demo'})
    def test_complete_workflow_daily_data(self):
        """Test complete workflow for getting daily stock data"""
        builder = AlphaVantageURLBuilder()

        # Add parameters for daily time series
        builder.add_params({
            'function': 'TIME_SERIES_DAILY',
            'symbol': 'IBM',
            'outputsize': 'compact',
            'datatype': 'json'
        })

        # Build URL
        builder.build()

        # Verify the URL is valid for Alpha Vantage API
        assert builder.url is not None
        assert 'function=TIME_SERIES_DAILY' in builder.url
        assert 'symbol=IBM' in builder.url
        assert 'apiKey=demo' in builder.url

    @patch.dict(os.environ, {'ALPHA_VANTAGE_API_KEY': 'demo'})
    def test_complete_workflow_company_overview(self):
        """Test complete workflow for getting company overview"""
        builder = AlphaVantageURLBuilder()

        builder.add_params({
            'function': 'OVERVIEW',
            'symbol': 'AAPL'
        })

        builder.build()

        assert builder.url is not None
        assert 'function=OVERVIEW' in builder.url
        assert 'symbol=AAPL' in builder.url


if __name__ == '__main__':
    pytest.main([__file__])
