import data
import sender_stand_request

def get_kit_body(name):
    body = data.kit_body.copy()
    body["name"] = name
    return body

def get_new_user_token():
    test_user = data.user_body.copy()
    response = sender_stand_request.post_new_user(test_user)
    resp_dict = response.json()
    return resp_dict["authToken"]

def positive_assert(kit_name):
    token = get_new_user_token()
    # Проверяется, что токен не пустой
    assert token != ""

    kit_body = get_kit_body(kit_name)
    kit_response = sender_stand_request.post_new_client_kit(kit_body, token)

    # Проверяется, что код ответа равен 201
    assert kit_response.status_code == 201

    # Проверяется, что в теле ответа имя пользователя такое же как было в запросе
    assert kit_response.json()["name"] == kit_name

def negative_assert(kit_name):
    token = get_new_user_token()
    # Проверяется, что токен не пустой
    assert token != ""

    is_empty_name = kit_name is None
    if is_empty_name:
        kit_body = {}
    else:
        kit_body = get_kit_body(kit_name)

    kit_response = sender_stand_request.post_new_client_kit(kit_body, token)
    #print(kit_response.status_code, kit_response.json())

    # Проверяется, что код ответа равен 400 для непустого имени набора
    if is_empty_name:
        # Проверяется, что код ответа равен 500 для пустого имени набора
        assert kit_response.status_code == 500
        # Проверяется, что сообщение об ошибке такое, как полагается для пустого набора
        assert kit_response.json()["message"] == 'null value in column "name" violates not-null constraint'
    else:
        # Проверяется, что код ответа равен 400 для непустого имени набора
        assert kit_response.status_code == 400

    # Проверка, что в теле ответа атрибут "code" равен status_code
    assert kit_response.status_code == kit_response.json()["code"]


def test_case1_single_letter_kit_name():
    positive_assert("a")

def test_case2_511_letters_kit_name():
    name_511 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    positive_assert(name_511)

def test_case3_empty_name_kit_name():
    negative_assert("")

def test_case4_512_letters_kit_name():
    name_512 = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    negative_assert(name_512)

def test_case5_latin_letters_kit_name():
    positive_assert("QWErty")

def test_case6_rus_letters_kit_name():
    positive_assert("Мария")

def test_case7_spec_chars_kit_name():
    positive_assert("\"№%@',")

def test_case8_with_spaces_kit_name():
    positive_assert(" Человек и КО ")

def test_case9_nums_kit_name():
    positive_assert("123")

def test_case10_no_name_kit_name():
    negative_assert(None)

def test_case11_number_kit_name():
    negative_assert(123)
