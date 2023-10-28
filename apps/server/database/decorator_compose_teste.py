def response(function):
    def wrapper(args):
        result = function(args)
        response_data = {"status": 200}
        response_data.update(result)
        return response_data

    return wrapper


@response
def funcao(email):
    return {"email": email}


print(funcao("marcus@email.com"))
