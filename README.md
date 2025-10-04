# Financial Data Q&A Assistant with RAG

A free, open-source financial question-answering system using Retrieval-Augmented Generation (RAG) powered by HuggingFace models and Polars for high-performance data processing.

## 🎯 Overview

This project builds an intelligent financial assistant that can answer questions about:
- **Market Data**: Stock prices, trading volumes, financial ratios
- **Company Analysis**: Revenue trends, earnings reports, financial health
- **Economic Indicators**: GDP, inflation, interest rates, market trends
- **Investment Concepts**: Portfolio theory, risk management, trading strategies
- **Financial Education**: Definitions, explanations, best practices

## 🚀 Features

- **100% Free**: Uses HuggingFace's free models and services
- **High Performance**: Polars-powered data processing (5-50x faster than Pandas)
- **Real-time Data**: Integration with financial APIs (Alpha Vantage, FRED, Yahoo Finance)
- **Intelligent Retrieval**: Semantic search using sentence transformers
- **Source Citations**: Transparent answers with document references
- **Streamlit UI**: Clean, interactive web interface
- **Scalable**: Handles large financial datasets efficiently

## 🏗️ Architecture

```
Financial APIs → Data Processing (Polars) → Document Chunking → 
Vector Embeddings → ChromaDB → RAG Pipeline → HuggingFace LLM → Streamlit UI
```
