#!/bin/bash
cd "$(dirname "$0")"
uv run python main.py "$@"
