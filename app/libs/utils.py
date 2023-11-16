from os.path import dirname
from urllib.parse import urlencode


def build_url(url: str, params: dict, new_page: int) -> str:
    base_url_with_path = dirname(url)
    params.update({"page": new_page})
    query_params = urlencode(params)
    if query_params:
        base_url_with_path += f"?{query_params}"
    return base_url_with_path
