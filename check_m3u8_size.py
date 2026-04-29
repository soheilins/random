import requests
from urllib.parse import urljoin

# Your M3U8 URL – hardcoded for one‑time use
M3U8_URL = 'https://d3stzm2eumvgb4.cloudfront.net/572ed3070a5b868a3534_spear_shot_316589965666_1777472867/720p60/index-muted-LPI91TX0ET.m3u8'

def get_total_size(m3u8_url):
    print(f"Fetching playlist: {m3u8_url}")
    resp = requests.get(m3u8_url)
    resp.raise_for_status()
    
    lines = resp.text.strip().splitlines()
    base_url = m3u8_url[:m3u8_url.rfind('/')+1]
    
    total_bytes = 0
    segment_count = 0
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            seg_url = urljoin(base_url, line)
            try:
                head = requests.head(seg_url, timeout=10)
                if head.status_code == 200:
                    size = int(head.headers.get('content-length', 0))
                    total_bytes += size
                    segment_count += 1
                    print(f"  {segment_count}: {seg_url.split('/')[-1]} -> {size/1024:.1f} KB")
                else:
                    print(f"  Warning: Could not fetch {seg_url} (HTTP {head.status_code})")
            except Exception as e:
                print(f"  Error on {seg_url}: {e}")
    
    return total_bytes, segment_count

if __name__ == '__main__':
    try:
        total_bytes, seg_count = get_total_size(M3U8_URL)
        total_mb = total_bytes / (1024 * 1024)
        
        print("\n" + "="*50)
        print(f"✅ Segments found: {seg_count}")
        print(f"✅ Total video size: {total_mb:.2f} MB ({total_bytes:,} bytes)")
        print("="*50)
    except Exception as e:
        print(f"❌ Failed: {e}")
        exit(1)
