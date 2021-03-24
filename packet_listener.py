import scapy.all as scapy
import optparse
from scapy_http import http

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface",help="Enter Interface")

    (user_input,argument) = parse_object.parse_args()

    if not user_input.interface:
        print(">> Enter Interface!")
        quit()

    return user_input


def listen_packets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyze_packets)
    #prn = callback function

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

user_interface = get_user_input()
listen_packets(user_interface.interface)