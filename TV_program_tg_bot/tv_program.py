import requests
from .model_tv_program import TV_program


def search(query: str):
    URL = f'https://api.tvmaze.com/singlesearch/shows?q={query}'
    res = requests.get(URL)
    return res.json(), res.status_code


def found_information_tv_program(tv_program: str):
    try:
        info_tv_program, status_code = search(tv_program)
    except Exception:
        raise Exception("Problems with the service")

    if status_code == 404:
        raise Exception(f"TV program ({tv_program}) not found.")

    try:
        tv_program = TV_program(**info_tv_program)
    except Exception:
        raise ValueError("Incorrect response.")

    return f"""Name: {tv_program.name}
Network Name: {tv_program.network.name}
Network Country Name: {tv_program.network.country.name}
Summary: {tv_program.summary}"""
