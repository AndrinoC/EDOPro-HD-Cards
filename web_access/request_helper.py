from typing import Any, Optional
import requests
from requests.exceptions import RequestException
from constants import REQUEST_HEADERS

def make_request(url: str, params: Optional[dict[str, Any]] = None, timeout: int = 10) -> requests.Response:
    """
    Makes a GET request with optional parameters and timeout.

    Args:
        url (str): The URL to make the request to.
        params (Optional[dict[str, Any]], optional): Optional query parameters. Defaults to None.
        timeout (int, optional): Timeout for the request in seconds. Defaults to 10.

    Returns:
        requests.Response: The response object.
    """
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, params=params, timeout=timeout)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx or 5xx)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {type(e).__name__} - {e}")
        raise  # Re-raise the exception for higher-level handling
    except Exception as e:
        print(f"Unexpected error making request to {url}: {type(e).__name__} - {e}")
        raise  # Re-raise the exception for higher-level handling
