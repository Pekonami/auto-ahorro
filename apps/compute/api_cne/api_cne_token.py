import http.client
import pathlib, dotenv

def main_api_cne_token():
    config = dotenv.dotenv_values(".env")

    my_email = config.get("correo")
    my_password = config.get("contrasena")

    conn = http.client.HTTPSConnection("api.cne.cl")

    payload = f"email={my_email}&password={my_password}"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    conn.request("POST", "/api/login", payload, headers)
    res = conn.getresponse()
    token_code = res.read()
    token = token_code.decode("utf-8")

    env_path = ".env"
    dotenv.set_key(dotenv_path=env_path, key_to_set="API_CNE", value_to_set=token[10:len(token) - 2])