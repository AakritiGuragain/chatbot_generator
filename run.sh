#!/bin/bash
PYTHONPATH=$(pwd):$(pwd)/src uv run streamlit run src/adapters/inbound/streamlit_adapter.py
