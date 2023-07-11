import requests

headers = {
    'content-type': 'application/json',
}

json_data = {
    'data': [
        'ok',
        [
            [
                'hi',
                "I'm sorry, but I'm not sure what you mean. Could you please provide more information so I can help you?",
            ],
        ],
    ],
    'event_data': None,
    'fn_index': 1,
    'session_hash': '6b5waetyyl',
}

response = requests.post('http://0.0.0.0:8000/run/predict', headers=headers, json=json_data)

if __main__ == '__name__':
    print(response.json())
