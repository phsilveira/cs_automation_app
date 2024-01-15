#!/bin/bash

export OPENAI_API_KEY=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
source /home/ai/customer_support/cs_automation_app/venv/bin/activate
source /home/ai/customer_support/cs_automation_app/.env
python3 /home/ai/customer_support/cs_automation_app/gradio_app.py >> /home/ai/customer_support/logs/gradio_app.log 2>&1