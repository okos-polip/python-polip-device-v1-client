import hashlib
import hmac
import time
from typing import Callable, Union
from .constants import POLIP_AWAIT_SERVER_OK_RECHECK_PERIOD

def format_version(major: int, minor: int, patch: int) -> str:
    return f"v{major}.{minor}.{patch}"

def block_await_server_ok(device: object, cb: Callable[[], None] = None, num_retries: Union[int, None] = None) -> None:
    print("Connecting to Okos Polip Device Ingest Service")

    count = 0

    def _check_server_status():
        nonlocal count
        if device.POLIP_OK == device.check_server_status():
            print("Connected")
            if cb:
                cb()
            return
        elif num_retries is not None and count >= num_retries:
            raise Exception("Number of retries exceeded")
        else:
            count += 1
            print("Failed to connect. Retrying...")
            time.sleep(POLIP_AWAIT_SERVER_OK_RECHECK_PERIOD)
            _check_server_status()

    _check_server_status()

def create_timestamp() -> int:
    return int(time.time() * 1000)

def create_tag(payload_str: str, client_key: str) -> str:
    key_bytes = bytes.fromhex(client_key)
    msg_bytes = payload_str.encode("utf-8")
    tag = hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()
    return tag

__all__ = ['format_version', 'block_await_server_ok', 'create_timestamp', 'create_tag']
