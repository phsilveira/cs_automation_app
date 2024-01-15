# CS Automation App (Streamlit and Gradio)

Streamlit and Gradio App for cs automation using CSV macro as input

Built with ❤️ by [phsilveira](https://github.com/phsilveira)

## Local Gradio setup
```sh
# External users: download Files
git clone git@github.com:phsilveira/cs_automation_app.git

# Go to correct directory
cd cs_automation_appq

# setup .env file
cp .env.example .env

# append the token in the .env file
echo "$(openssl rand -hex 32)" >> .env

python gradio_app.py
```

## Local Gradio Setup Using Docker
```sh
# Start the docker container and build the image
docker-compose up -d --build
```

## CURL Request
```sh
curl 'http://0.0.0.0:8000/run/predict' \
  -H 'content-type: application/json' \
  -H 'Authorization: Bearer TOKEN' \
  --data-raw $'{"data":["hi",[], "flingster"],"fn_index":1,"session_hash":"6b5waetyyl"}' \
  --compressed
```


## API Documentation

### Endpoint: `/run/predict`

#### Request

- Method: POST
- URL: `http://0.0.0.0:8000/run/predict`
- Headers:
  - Content-Type: application/json.
  - Authorization: Bearer TOKEN - Provides authentication using a bearer token. Replace TOKEN with the actual token value within the .env file.


##### Request Body

```json
{
  "data": [
    "hi",
    [],
    "flingster"
  ],
  "fn_index": 1,
  "session_hash": "6b5waetyyl"
}
```

- `data` (Array):
  - The first element is the input message (String).
  - The second element is an array of history messages (Array of Arrays of Strings).
  - The third element is the name of the brand (String).

- `fn_index` (Integer):
  - Index of a specific function (Integer).

- `session_hash` (String):
  - Hash value representing the session (String).

#### Response

- Content-Type: application/json

##### Response Body

```json
{
  "data": [
    "",
    [
      ["hi", "Hi there, how can I help you?"]
    ]
  ],
  "is_generating": false,
  "duration": 3.4465811252593994,
  "average_duration": 3.4465811252593994
}
```

- `data` (Array):
  - The first element is the input message (String).
  - The second element is an array of history messages (Array of Arrays of Strings).

- `is_generating` (Boolean):
  - Indicates whether the response is being generated (Boolean).

- `duration` (Float):
  - The time taken to generate the response in seconds (Float).

- `average_duration` (Float):
  - The average time taken to generate the response in seconds (Float).

Please refer to the API documentation for more detailed information about the endpoint and its functionality.


### Local Development

The `Makefile` and development requirements provide some handy Python tools for writing better code.
See the `Makefile` for more detail

```sh
# Run black, isort, and flake8 on your codebase
make lint
# Run pytest with coverage report on all tests not marked with `@pytest.mark.e2e`
make test
# Run pytest on tests marked e2e (NOTE: e2e tests require `make run` to be running in a separate terminal)
make test-e2e
# Run pytest on tests marked e2e and replace visual baseline images
make test-e2e-baseline
# After running tests, display the coverage html report on localhost
make coverage
```
## Deploy

I recommend use docker-compose to deploy this app. You can use the docker-compose.yml file in this repo as a template.
  
```sh
docker-compose up -d --build
```

## What's this?

- `README.md`: This Document! To help you find your way around
- `streamlit_app.py`: The main app that gets run by [`streamlit`](https://docs.streamlit.io/)
- `requirements.txt`: Pins the version of packages needed
- `LICENSE`: Follows Streamlit's use of Apache 2.0 Open Source License
- `.gitignore`: Tells git to avoid comitting / scanning certain local-specific files
- `.streamlit/config.toml`: Customizes the behaviour of streamlit without specifying command line arguments (`streamlit config show`)
- `Makefile`: Provides useful commands for working on the project such as `run`, `lint`, `test`, and `test-e2e`
- `requirements.dev.txt`: Provides packages useful for development but not necessarily production deployment. Also includes all of `requirements.txt` via `-r`
- `pyproject.toml`: Provides a main configuration point for Python dev tools
- `.flake8`: Because `flake8` doesn't play nicely with `pyproject.toml` out of the box
- `.pre-commit-config.yaml`: Provides safeguards for what you commit and push to your repo
- `tests/`: Folder for tests to be picked up by `pytest`

## Credits

This package was created with Cookiecutter and the `gerardrbentley/cookiecutter-streamlit` project template.

- Cookiecutter: [https://github.com/audreyr/cookiecutter](https://github.com/audreyr/cookiecutter)
- `gerardrbentley/cookiecutter-streamlit`: [https://github.com/gerardrbentley/cookiecutter-streamlit](https://github.com/gerardrbentley/cookiecutter-streamlit)
