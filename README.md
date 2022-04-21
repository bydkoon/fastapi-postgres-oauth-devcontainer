
# Start Development Containers: Fastapi-postgres-oauth-devcontiner

[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/vscode-remote-try-python)

Go to the [Google API & Services Dashboard](https://console.cloud.google.com/apis/dashboard)


First, copy `.env.sample` to `.env`:

    $ cp .env.sample .env

- Set up the env vars:
    - export GOOGLE_CLIENT_ID=...
    - export GOOGLE_CLIENT_SECRET=...
    - export SECRET_KEY=...
    - export API_SECRET_KEY=...

Create your Google OAuth Client and fill the client ID and secret
into `.env`, then run:
When register your Google OAuth Client, remember to put:

    http://127.0.0.1:8000/

into the client redirect urls

## version
- Python3.9+

## docker devcontainer File sharing add

 - docker settings → Resource → File sharing  → project directory

