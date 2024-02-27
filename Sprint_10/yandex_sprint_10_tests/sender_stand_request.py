import configuration
import requests
import data

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
                         json=body,  # тут тело
                         headers=data.headers)  # а здесь заголовки

def post_new_client_kit(kit_body, auth_token):
    headers = data.kit_headers.copy()
    headers["Authorization"] = "Bearer " + auth_token
    #print(kit_body, headers)
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KIT_PATH,  # подставляем полный url
                         json=kit_body,  # тут тело
                         headers=headers)  # а здесь заголовки


# пробные вызовы функций post_new_user() и post_new_client_kit()
test_user = data.user_body.copy()
response = post_new_user(test_user)
print(response.status_code)

resp_dict = response.json()
auth_token = resp_dict["authToken"]

test_kit = data.kit_body.copy()
response = post_new_client_kit(test_kit, auth_token)
print(response.status_code, response.text)
