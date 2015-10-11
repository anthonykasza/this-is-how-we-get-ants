# modified from https://thepacketgeek.com/scapy-p-09-scapy-and-dns/

from scapy.all import *

listen_ip = "10.0.0.1"
filter = "udp port 53 and ip dst " + listen_ip + " and not ip src " + listen_ip

def handler(i):

  def relay_dns(orig_pkt):
    ip = IP(dst="8.8.8.8")
    udp = UDP(sport=orig_pkt[UDP].sport)
    dns = DNS(rd=1,id=orig_pkt[DNS].id,qd=DNSQR(qname=orig_pkt[DNSQR].qname))
    resp = sr1(ip / udp / dns, verbose=0)      

    resp_pkt = IP(dst=orig_pkt[IP].src) / UDP(dport=orig_pkt[UDP].sport) / DNS()    
    resp_pkt[DNS] = resp[DNS]
    send(resp_pkt, verbose=0)

  return relay_dns

sniff(filter=filter, prn=handler(1))
