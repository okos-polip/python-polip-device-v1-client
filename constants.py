POLIP_DEVICE_INGEST_SERVER_ADDRESS = "api.okospolip.com"
POLIP_DEVICE_INGEST_SERVER_HTTP_PORT = 3021
POLIP_DEVICE_INGEST_SERVER_HTTPS_PORT = 3022

POLIP_DEVICE_INGEST_SERVER_URL = f"http://{POLIP_DEVICE_INGEST_SERVER_ADDRESS}:{POLIP_DEVICE_INGEST_SERVER_HTTP_PORT}"
POLIP_DEVICE_INGEST_SERVER_URL_SECURE = f"https://{POLIP_DEVICE_INGEST_SERVER_ADDRESS}:{POLIP_DEVICE_INGEST_SERVER_HTTPS_PORT}"

POLIP_DEFAULT_POLL_STATE_PERIOD = 1000
POLIP_DEFAULT_PUSH_SENSE_PERIOD = 1000
POLIP_AWAIT_SERVER_OK_RECHECK_PERIOD = 500

__all__ = [
    'POLIP_DEVICE_INGEST_SERVER_ADDRESS',
    'POLIP_DEVICE_INGEST_SERVER_HTTP_PORT',
    'POLIP_DEVICE_INGEST_SERVER_HTTPS_PORT',
    'POLIP_DEVICE_INGEST_SERVER_URL',
    'POLIP_DEVICE_INGEST_SERVER_URL_SECURE',
    'POLIP_DEFAULT_POLL_STATE_PERIOD',
    'POLIP_DEFAULT_PUSH_SENSE_PERIOD',
    'POLIP_AWAIT_SERVER_OK_RECHECK_PERIOD'
]