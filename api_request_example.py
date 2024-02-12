import requests

headers = {
    "content-type": "application/json",
    "Authorization": "Bearer 65447b789ef4f9108253353c7d82d7af89affee16bef070f648e63411839f56b"
}

json_data = {
    "data": [
        "why i was banned?",
        [
            [
                "hi",
                "How can I help you?",
            ],
        ],
        "flingster",
        {
            "vip_details": {
                "payment_processor": "SegPay",
                "vip": True,
                "will_rebill_at": 1706937877,
                "canceled_at": 0,
                "remaining_vip_days": 6,
                "description": "VIP Since: 2024-01-27 05:24:37 (today)  Next bill: 2024-02-03 05:24:37 (in 7 days)"
            },
            "ban_details": {
                "ban_id": 123456,
                "reason": "Nudity or simulated sexual acts",
                "expires": 1706937877,
                "can_verify": False
            }
        },
    ],
    "fn_index": 1,
    "session_hash": "6b5waetyyl",
}

if __name__ == "__main__":
    response = requests.post(
        "http://localhost:8000/run/predict", headers=headers, json=json_data
    )
    print(response.json())
