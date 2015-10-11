This Is How We Get Ants
=======================


What is?
--------
A hacky DNS tunnel built with Scapy. It takes advantage of the DNS protocols lack of a length field. This tunneling mechanism likely won't survive beyond a recursive resolver so limit your internal network's direct Internet access to mitigate.

How do?
-------
- *get_topsites.sh* downloads the Alexa top 1m file and uses it to write the top 1000 domain names to a file called topsites.txt
- *topsites.txt* contains the top 1000 domain names
- *file.dat* is a fake malware beacon containing fake system information
- *client.py* is a script with reads the topsites.txt and file.dat files into memory. It base64 encodes the file.dat data in memory. It then randomly selects names from the topsites file and issues DNS queries for those sites with chunks of the encoded file.dat embedded into it. It then sleeps. It then issues a final DNS query for icanhazip.com to similate executing the Upatre sample.
- *server.py* sniffs for incoming DNS queries, forwards them on to 8.8.8.8 and relays the response.

What's Left?
------------
- figure out how to send things back from server to client
  - perhaps a special use domain name for signaling?

Where else?
-----------
[PSUDP](https://media.blackhat.com/bh-us-10/whitepapers/Born/BlackHat-USA-2010-Born-psudp-Passive-Network-Covert-Communication-wp.pdf)
