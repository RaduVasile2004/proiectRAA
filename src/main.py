from traceroute import traceroute
import socket
import json

destinations = {
    "China (.cn)": "www.baidu.cn",
    "Africa (.za)": "www.gov.za",
    "Australia (.au)": "www.abc.net.au"
}

for label, domain in destinations.items():
    print(f"\n== Traceroute către {label} ({domain}) ==")
    try:
        ip = socket.gethostbyname(domain)
        result = traceroute(ip)
        filename = f"trace_{label.replace(' ', '_').replace('.', '')}.json"
        with open(filename, "w") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        print(f"Failed to trace {domain}: {e}")

