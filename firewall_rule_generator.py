import ipaddress, sys, platform

def generate_firewall_rule(source_ip, destination_ip, port, action):

    # Check validity of  source IP
    try:
        source_ip = ipaddress.ip_network(source_ip)
    except ValueError:
        return None

    # Check validity of destination IP
    try:
        destination_ip = ipaddress.ip_network(destination_ip)
    except ValueError:
        return None

    # Generate firewall rule based on OS
    if platform.system() == "Windows":
        rule = f"Windows: netsh advfirewall firewall add rule name=\"Custom Rule\" dir=in action={action} localport={port} protocol=TCP remoteip={source_ip}"
    else:
        rule = f"Linux: iptables -A INPUT -s {source_ip} -d {destination_ip} -p tcp --dport {port} -j {action}"

    return rule


source_ip = input("Enter the source IP (in CIDR notation): ")
destination_ip = input("Enter the destination IP (in CIDR notation): ")
port = input("Enter the port: ")
action = input("Enter the action (ACCEPT or DROP): ")

firewall_rule = generate_firewall_rule(source_ip, destination_ip, port, action)
if firewall_rule:
    print(f"Generated firewall rule: \n {firewall_rule}")
else:
    print("Invalid input. Please try again.")