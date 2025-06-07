import socket
import struct
import time
import requests

def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {
            "ip": ip,
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "lat": data.get("lat"),
            "lon": data.get("lon")
        }
    except Exception as e:
        print(f"Failed to get location for {ip}: {e}")
        return {
            "ip": ip,
            "city": None,
            "region": None,
            "country": None,
            "lat": None,
            "lon": None
        }

def traceroute(dest_ip, port=33434, max_hops=30, timeout=3):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_sock.settimeout(timeout)

    result = []

    for ttl in range(1, max_hops + 1):
        udp_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        try:
            udp_sock.sendto(b'', (dest_ip, port))
            start_time = time.time()

            data, addr = icmp_sock.recvfrom(512)
            elapsed = (time.time() - start_time) * 1000  # ms

            hop_ip = addr[0]
            location = get_ip_location(hop_ip)
            location['ttl'] = ttl
            location['elapsed'] = round(elapsed, 2)
            result.append(location)

            print(f"{ttl:2d}: {hop_ip} - {location['city']}, {location['region']}, {location['country']} [{location['elapsed']} ms]")

            if hop_ip == dest_ip:
                break

        except socket.timeout:
            print(f"{ttl:2d}: * (timeout)")
            result.append({
                "ttl": ttl,
                "ip": "*",
                "city": None,
                "region": None,
                "country": None,
                "lat": None,
                "lon": None,
                "elapsed": None
            })

    udp_sock.close()
    icmp_sock.close()
    return result

