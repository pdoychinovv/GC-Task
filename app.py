import time
import requests
from prometheus_client import start_http_server, Gauge

URLS = [
    {"url": "https://httpstat.us/503"},
    {"url": "https://httpstat.us/200"}
]

# Prometheus metrics
url_up = Gauge('sample_external_url_up', 'URL availability', ['url'])
url_response_ms = Gauge('sample_external_url_response_ms', 'URL response time in milliseconds', ['url'])

def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        elapsed_ms = (time.time() - start_time) * 1000
        return (1 if response.status_code == 200 else 0), elapsed_ms
    except requests.RequestException:
        return 0, 0

def update_metrics():
    for entry in URLS:
        up, latency = check_url(entry["url"])
        print(f"Checked {entry['url']} - up={up}, latency={latency:.2f}ms")
        url_up.labels(url=entry["url"]).set(up)
        url_response_ms.labels(url=entry["url"]).set(latency)

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        update_metrics()
        time.sleep(5)

