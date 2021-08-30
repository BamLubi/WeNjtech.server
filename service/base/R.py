import json

response = {
    "code": None,
    "data": None,
    "mark": None,
}

def OK(data, mark):
    response["code"] = 200
    response["data"] = data
    response["mark"] = mark
    return json.dumps(response, ensure_ascii=False)


def FAIL(data, mark):
    response["code"] = 400
    response["data"] = data
    response["mark"] = mark
    return json.dumps(response, ensure_ascii=False)