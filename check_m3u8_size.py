import os
import requests
from urllib.parse import urljoin

M3U8_URL = os.getenv('M3U8_URL', 'https://d3stzm2eumvgb4.cloudfront.net/572ed3070a5b868a3534_spear_shot_316589965666_1777472867/720p60/index-muted-LPI91TX0ET.m3u8')  # or paste directly

def get_total_size(m3u8_url):
    resp = requests.get(m3u8_url)
    resp.raise_for_status()
    lines = resp.text.strip().splitlines()
    base_url = m3u8_url[:m3u8_url.rfind('/')+1]
    total = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            seg_url = urljoin(base_url, line)
            head = requests.head(seg_url)
            total += int(head.headers.get('content-length', 0))
    return total

if __name__ == '__main__':
    total_bytes = get_total_size(M3U8_URL)
    total_mb = total_bytes / (1024 * 1024)
    print(f"\n✅ Total video size: {total_mb:.2f} MB ({total_bytes} bytes)")
