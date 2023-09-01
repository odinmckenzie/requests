# My Requests Library Fork

This fork of the popular `requests` library introduces a new feature that allows you to specify the number of retry attempts via a `retries` parameter. This parameter is available in the following methods:

- `requests.get()`
- `requests.head()`
- `requests.post()`
- `requests.patch()`
- `requests.put()`
- `requests.options()`
- `requests.request()`

## Installation

```bash
pip install -e git+https://github.com/odinmckenzie/requests.git#egg=requests
```

## Basic Usage

You can use the `retries` parameter with an integer value to indicate the number of retry attempts.

### With Integer

The following example will attempt to make a GET request up to 3 times before giving up.

```python
import requests
from requests.exceptions import ConnectTimeout

try:
    response = requests.get('http://10.1.1.1:8765/', timeout=0.25, retries=3)
except ConnectTimeout as e:
    # for retries=3 it will send 4 requests
    print("num_requests_sent: ", e.args[0].pool.num_requests)
```

Expected output:
```python
num_requests_sent: 4
```

### With `urllib3.util.retry.Retry`

For more fine-grained control, you can pass in a `Retry` object from `urllib3.util.retry`. This allows you to specify different policies for different types of errors. In this example, the request will be retried up to 3 times for the specified HTTP status codes, with a backoff factor of 1 between each retry.

```python
import requests
from urllib3.util.retry import Retry
from requests.exceptions import RetryError

# Create a Retry object
retry_strategy = Retry(
    total=3, #number of retries
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)

try:
    response = requests.get('http://httpbin.org/status/503', retries=retry_strategy)
except RetryError as e:
    # for total=3 it will send 4 requests
    print("num_requests_sent: ", e.args[0].pool.num_requests)
```

Expected output:
```python
num_requests_sent: 4
```

## Additional Usage

The `retries` parameter can also be used with the following methods of the `Session` object from `requests.sessions`:

- `get()`
- `head()`
- `post()`
- `patch()`
- `put()`
- `request()`

The example will attempt to make a GET request up to 3 times before giving up.

```python
import requests
from requests.exceptions import ConnectTimeout
from requests.sessions import Session

session = Session()

try:
    response = session.request('GET', 'http://10.1.1.1:8765/', timeout=0.25, retries=3)
except ConnectTimeout as e:
    # for retries=3 it will send 4 requests
    print("num_requests_sent: ", e.args[0].pool.num_requests)
```

Expected output:
```python
num_requests_sent: 4
```

The [documentation](https://requests.readthedocs.io/en/latest/user/advanced/#example-automatic-retries) for Requests suggested a solution for retrying failed connections. The solution shown below still works.

```python
import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from urllib3.util.retry import Retry

s = Session()
retries = Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={'GET'},
)
s.mount('https://', HTTPAdapter(max_retries=retries))

try:
    response = s.get('https://httpbin.org/status/503')
except RetryError as e:
    # for retries=3 it will send 4 requests
    print("num_requests_sent: ", e.args[0].pool.num_requests)
```

## Limitations

The methods `post()` and `patch()` only retry on a connection error and not for any specified HTTP status codes. This is because of implementation details in the `urllib3` library.
