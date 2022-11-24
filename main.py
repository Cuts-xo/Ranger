import ipaddress
import requests
import socket
from pprint import pprint
asn = str(input("ASN: "))
if "AS" not in asn:
    asn = "AS" + asn

url_base = 'http://ipinfo.io/'
prefixes = []
r = requests.get(f"https://stat.ripe.net/data/announced-prefixes/data.json?resource={asn}&starttime=2011-12-12T12:00").json()
r = r['data']
r = r['prefixes']
for i in r:
    prefix = i['prefix']
    if ":" not in prefix:
        prefixes.append(prefix)


print("Successfully found prefixes.")
iplist = open("list.txt", "a+")

for prefix in prefixes:
    for ip in ipaddress.IPv4Network(prefix):
        iplist.write(str(ip) + "\n")
    print(prefix + " Successfully written to file.")
iplist.close()
iplist = open("list.txt", "r")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
for ip in iplist.readlines():
    if ip != "":
        try:
            check = sock.connect_ex((ip, 80))
            port = 80
        except:
            try:
                check = sock.connect_ex((ip, 443))
                port = 443
            except:
                print("skipping ip " + ip)
                check = 1
        if check == 0:
            print(f"HIT! http://{ip}:{port}")
