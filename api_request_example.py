import requests

headers = {
    "content-type": "application/json",
    "Authorization": "Bearer 6b34cdc1876d17947d7210164d62fcd1f725c87ff0e71933e82ad3dec45e8b3f"
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
        "flingster"
    ],
    "fn_index": 1,
    "session_hash": "6b5waetyyl",
}

if __name__ == "__main__":
    response = requests.post(
        "http://192.168.0.116:8000/run/predict", headers=headers, json=json_data
    )
    print(response.json())
