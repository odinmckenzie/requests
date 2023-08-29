import pytest
import requests
from requests.exceptions import ConnectTimeout, RetryError
from urllib3.util.retry import Retry


def test_number_of_retries_with_get():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.get("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_number_of_retries_with_post():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.post("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_number_of_retries_with_patch():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.patch("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_number_of_retries_with_put():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.post("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_number_of_retries_with_head():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.head("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_number_of_retries_with_options():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.options("http://10.1.1.1:8765/", timeout=0.25, retries=2)
    
    # for retries=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3

def test_default_number_of_retries_with_get():
    with pytest.raises(ConnectTimeout) as excinfo:
        requests.get("http://10.1.1.1:8765/", timeout=0.25)
    
    # By default Requests does not retry failed connections.
    assert excinfo.value.args[0].pool.num_requests == 1

def test_retry_obj_with_get():
    retry_strategy = Retry(
        total=2,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    with pytest.raises(RetryError) as excinfo:
        requests.get("https://httpbin.org/status/429", retries=retry_strategy)
    
    # for total=2 it should send 3 requests
    assert excinfo.value.args[0].pool.num_requests == 3
