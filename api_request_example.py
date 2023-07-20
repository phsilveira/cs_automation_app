import requests

headers = {
    "content-type": "application/json",
}

json_data = {
    "data": [
        "I want a refund",
        [
            [
                "hi",
                "How can I help you?",
            ],
        ],
    ],
    "fn_index": 1,
    "session_hash": "6b5waetyyl",
}

if __name__ == "__main__":
    response = requests.post(
        "http://0.0.0.0:8000/run/predict", headers=headers, json=json_data
    )
    print(response.json())
