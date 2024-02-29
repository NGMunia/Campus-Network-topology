
# Campus-Network-Topology

The following topology demonstrates a hierarchical network topology with a collapsed core while employing software-defined networking (Automation).

The Branch networks are linked with a single-hub DMVPN for site-to-site VPN connectivity. 
The network is also configured as BGP-AS-64511 as a non-transit Network, with ISPs only advertising a default route to the HQ site.

![Topology](/Network/Topology.png)


## Layer 2 connectivity:
The network Employs various layer 2 protocols namely:


**LACP**:

CORE switches and Access switches are configured with LACP in active-active mode.
Verification is seen below on the ACC-SW1:


``` bash
ACCESS-SWITCH-1#sh etherchannel summary
! Output omitted for brevity
Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+------------------------
1      Po1(SU)         LACP      Et1/0(P)    Et1/1(P)
2      Po2(SU)         LACP      Et1/2(P)    Et1/3(P)

```

**Rapid PVST+ and Load balancing**:

CORE-SW-1 acts as the root bridge for both VLAN-10 and VLAN-11 traffic and CORE-SW-2 acts as the root bridge for VLAN-12.

Porfast and BPDUguard features are enabled on all access switchports.

``` bash
CORE-SWITCH-1#sh spanning-tree summary totals
Switch is in rapid-pvst mode
Root bridge for: VLAN0001, VLAN0010-VLAN0011

CORE-SWITCH-2#sh spanning-tree summary totals
Switch is in rapid-pvst mode
Root bridge for: VLAN0012
```


## Layer 3 connectivity:
The network Employs various layer 3 protocols namely:


**InterVLAN Routing**:

The network topology is designed as a collapsed core, where the core switches assume the responsibilities of both the core and distribution layers. 

InterVLAN routing is configured, enabling communication between different VLANs within the network.

To enhance network resilience and load sharing, in InterVLAN routing HSRPv2 is implemented.

```bash
CORE-SWITCH-1#sh standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Vl10        10   110 P Active  local           192.168.10.2    192.168.10.3
Vl11        11   110 P Active  local           192.168.11.2    192.168.11.3
Vl12        12   100 P Standby 192.168.12.2    local           192.168.12.3

CORE-SWITCH-2#sh standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Vl10        10   100 P Standby 192.168.10.1    local           192.168.10.3
Vl11        11   100 P Standby 192.168.11.1    local           192.168.11.3
Vl12        12   110 P Active  local           192.168.12.1    192.168.12.3
```

**Multi-Area OSPF**:

In the HQ region, OSPF is implemented to manage and optimize the routing infrastructure. 
The network architecture employs inter-area OSPF, specifically designed to enhance scalability and manageability through the segmentation of the network into designated areas.

By utilizing OSPF as the routing protocol and implementing inter-area OSPF, the network achieves a more modular and organized structure. 
Each designated area within the HQ region can operate independently, allowing for improved network performance, reduced routing overhead, (controlled LSA propagation).

```bash
Sample config
CORE-SWITCH-1#sh ip route ospf
!
Gateway of last resort is 10.0.0.2 to network 0.0.0.0

O*E2  0.0.0.0/0 [110/1] via 10.0.0.2, 02:10:04, Ethernet2/0
      10.0.0.0/8 is variably subnetted, 12 subnets, 3 masks
O        10.0.0.4/30 [110/30000] via 10.0.20.2, 02:09:44, Ethernet1/0
O        10.0.20.4/30 [110/20000] via 10.0.20.2, 02:09:44, Ethernet1/0
O IA     10.0.51.0/30 [110/20000] via 10.0.0.2, 02:10:04, Ethernet2/0
O IA     10.0.51.12/30 [110/40000] via 10.0.20.2, 02:09:44, Ethernet1/0
O E2     10.1.10.0/23 [110/20] via 10.0.0.2, 02:08:41, Ethernet2/0
O E2     10.1.20.0/23 [110/20] via 10.0.0.2, 02:08:37, Ethernet2/0
O IA  192.168.20.0/24 [110/20000] via 10.0.20.2, 02:09:44, Ethernet1/0
CORE-SWITCH-1#


```

**EIGRP**:

Within the network infrastructure, EIGRP is deployed to facilitate routing within mGRE tunnels, specifically configured under DMVPN architecture.

To enhance the efficiency of the network, spokes within the mGRE tunnels are optimized as stub routers. 
This minimizes the likelihood of Stuck-in-Active scenarios.

Use of MD5 authentication, ensuring the integrity and authenticity of EIGRP messages exchanged within the mGRE tunnels. 

Bandwidth optimization feature is employed to limit EIGRP bandwidth usage.

The bandwidth metric (K3) is configured as the only metric to be used in path calculation.

```bash
Sample config:

BRANCH-A-ROUTER-2#sh running-config | s r e
router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface Tunnel10
   summary-address 10.1.10.0 255.255.254.0
   authentication mode md5
   authentication key-chain EIGRP-KEY
   bandwidth-percent 25
  exit-af-interface
  !
  af-interface Ethernet0/0.10
   passive-interface
  exit-af-interface
  !
  af-interface Ethernet0/0.11
   passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 10.1.10.0 0.0.0.255
  network 10.1.11.0 0.0.0.255
  network 172.20.0.0 0.0.0.255
  metric weights 0 0 0 1 0 0 0
  eigrp stub connected summary
 exit-address-family
```


**BGP**:

BGP peering is formed between EDGE routers and their connected ISPs.
Within the HQ's network architecture, BGP is implemented with a focus as a non-transit site. 
In a non-transit scenario, the network primarily manages its own routes and communicates with external networks, but does not forward traffic on behalf of third-party networks.

The design also involves the propagation of only a default BGP route to the Campus network from the ISPs.
This reduces the size of the BGP routing table.


To optimize the distribution of BGP traffic and ensure load-sharing, egress traffic is directed to exit through the Edge-1 router, by use of HSRPv2. 
To enable **automatic fail-over**, HSRP is configured in conjunction with IP-SLA and object tracking to track reachability of 44.67.28.1/32

Ingress traffic is routed through Edge-2 by applying AS-prepending to  32.19.86.0/24 prefix on Edge-1 outbound, influencing the inbound traffic flow through Edge-2 as a better path.


```bash
router bgp 64511
 bgp log-neighbor-changes
 network 32.19.86.0 mask 255.255.255.0
 neighbor 44.67.28.1 remote-as 100
 neighbor 44.67.28.1 route-map AS-prepending-map out
 neighbor 44.67.28.1 filter-list 10 out
!
ip as-path access-list 10 permit ^$
!
route-map AS-prepending-map permit 10
 match as-path 10
 set as-path prepend 64511 64511
```

**Redistribution**:

OSPF redistribution, Redistributes EIGRP spoke LAN prefixes into the OSPF domain.
EIGRP redistribution: Redistributes Area 20 and VLAN 12 prefixes into EIGRP.
DMVPN-ROUTER is responsible for redistribution between OSPF and EIGRP domain.
The EIGRP Add-path feature enables redundant prefix advertisement for 10.1.10.0/23 and 10.1.20.0/23 prefixes.

```bash

BRANCH-A-ROUTER-1#sh ip route eigrp
      10.0.0.0/8 is variably subnetted, 6 subnets, 3 masks
D        10.1.10.0/23 is a summary, 00:00:17, Null0
D        10.1.20.0/23 [90/522240] via 172.20.0.5, 00:00:20, Tunnel10
                      [90/522240] via 172.20.0.4, 00:00:20, Tunnel10
D EX  192.168.12.0/24 [170/56320] via 172.20.0.1, 00:00:12, Tunnel10
D EX  192.168.20.0/24 [170/56320] via 172.20.0.1, 00:00:12, Tunnel10


FW-MANAGEMENT-ZONE#sh ip route ospf

O E2     10.1.10.0/23 [110/20] via 10.0.20.5, 02:26:20, Ethernet0/3
                      [110/20] via 10.0.20.1, 02:26:16, Ethernet0/2
O E2     10.1.20.0/23 [110/20] via 10.0.20.5, 02:26:10, Ethernet0/3
                      [110/20] via 10.0.20.1, 02:26:12, Ethernet0/2
```

## Automating the Network:
The SDN controller is hosted on an Ubuntu server, serving as a centralized platform for orchestrating network configurations. 
Its primary function is to manage and automate network tasks through Python scripts.
Python uses Netmiko library.
Netmiko relies on SSH as its Southbound Interface for communication with network devices. 

```bash
# Update the package list
sudo apt-get update

# Upgrade installed packages
sudo apt-get upgrade

# Install pip for Python 3
sudo apt-get install python3-pip

# Install netmiko using pip
pip install netmiko

# Install Jinja2
pip install jinja2
```

Sample code snippet of getting Network device **running configuration** using Netmiko library:

```python
'Router':{
         'device_type':'cisco_ios',
         'username': Username,
         'secret': Secret,
         'password': Password,
         'ip':'10.1.10.1'
         }
c = ConnectHandler(**Router)
c.enable()
print(c.send_command('show run'))

```

#### JINJA2


Jinja2 is a templating engine that allows you to create dynamic templates with placeholders for variables.

When combined with network automation tools like Netmiko Jinja2 helps streamline the configuration process for multiple devices.

First, you'll create a Jinja2 template that contains placeholders for the variables you want to use.

To define a variable in a Jinja2 template, you use the **{{ }} syntax**.

Example: 
```bash
#Intf_template:
  interface {{Interface_name}} 
  Description {{Description}} 
  ip address {{Address}} {{Netmask}} 
  no shut
```

**Parsing Data to the Template**

When rendering a Jinja2 template, you provide a dictionary or an object containing the data you want to use for variable substitution.
The keys in the dictionary correspond to the variable names in the template.

Example:
```python
data = {
        'interface':'e0/1',
        'Description':'Connected to Core-SW-1',
        'ip address':'192.168.1.1 255.255.255.0'
       }
```
During template rendering, Jinja2 replaces the variables in the template with their corresponding values from the data dictionary.
The Environment class in Jinja2 manages the template configurations, including:
  * **_templates loading_**: It knows where to find your templates (templates directory)
 * **_FileSystemLoader_** is a template loader in Jinja2 that loads templates from the file system. It searches for templates in a specified directory on the file system and loads them when requested.
  * **_templates rendering_**: It knows how to take your templates and replace the placeholders with the actual values you provide in the data dictionary
 
```python
#Template Loading:
template_dir = input('Input directory path:')
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(intf_template.j2)

#Template Rendering:
commands = template.render(data.splitlines())
```

With this now you can integrete with NetMiko to configure a device.

```python
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

c = ConnectHandler(**Router)
c.enable()

#data
data = {
        'interface':'e0/1',
        'Description':'Connected to Core-SW-1',
        'ip address':'192.168.1.1 255.255.255.0'
       }
template_dir = input('Input directory path:')

# Find the template directory and load the template "intf_template"
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(intf_template.j2)

# Takes the template and replaces the placeholders with the actual data in the "data" dictionary
commands = template.render(data)

# send and print the commands to the Router using ConnectHandler
print(c.send_config_set(commands))
```

**Automating Backup using EEM**

Embedded event manager can be used to automate network devices' tasks.
In this case, EEM is used to automate backup of start-up configs on a scheduled basis; every Mon to Sat
at 1430hrs.

```bash
event manager environment tftpserver tftp://192.168.12.100/
event manager environment filename SW_BR_2.txt
event manager applet Automatic_Backup_Config
 event timer cron cron-entry "30 14 * * 1-6"
 action 1.0 cli command "enable"
 action 1.1 cli command "debug event manager action cli"
 action 1.2 cli command "conf t"
 action 1.3 cli command "file prompt quiet"
 action 1.4 cli command "do copy start $tftpserver$filename"
 action 1.5 cli command "no file prompt quiet"
 action 1.6 syslog priority informational msg "TFTP backup successful"
```


## VPN Services:
DMVPN phase 2 with IPsec is used to secure communications between the HQ and the Branch spokes.
EIGRP is the protocol of choice for routing through the mGRE tunnel.

```bash
DMVPN-HUB-ROUTER#sh ip route eigrp

Gateway of last resort is 32.19.86.3 to network 0.0.0.0

      10.0.0.0/8 is variably subnetted, 10 subnets, 3 masks
D        10.1.10.0/23 [90/517120] via 172.20.0.3, 00:30:26, Tunnel10
                      [90/517120] via 172.20.0.2, 00:30:26, Tunnel10
D        10.1.20.0/23 [90/517120] via 172.20.0.5, 00:27:24, Tunnel10
                      [90/517120] via 172.20.0.4, 00:27:24, Tunnel10


DMVPN-HUB-ROUTER#sh crypto isakmp sa
IPv4 Crypto ISAKMP SA
dst             src             state          conn-id status
32.19.86.254    44.67.28.6      QM_IDLE           1003 ACTIVE
32.19.86.254    72.73.74.10     QM_IDLE           1004 ACTIVE
32.19.86.254    44.67.28.10     QM_IDLE           1001 ACTIVE
32.19.86.254    72.73.74.6      QM_IDLE           1002 ACTIVE


```

## Network Security:

**Zone-Based Firewalls**
Zone-based firewall services are configured on the Edge-Firewall (FW-EDGE) with stateful traffic inspection from Inside(Private network) to the Internet.
```bash
FIREWALL-EDGE#sh policy-map type inspect zone-pair private-Internet-zone

policy exists on zp Private-Internet-zone
  Zone-pair: Private-Internet-zone

  Service-policy inspect : Private-Internet-policy

    Class-map: Private-Internet-class (match-all)
      Match: access-group name Private-Internet-acl

   Inspect
        Packet inspection statistics [process switch:fast switch]
        tcp packets: [1276:0]
        udp packets: [1296:0]
        icmp packets: [8:0]

        Session creations since subsystem startup or last reset 116
        Current session counts (estab/half-open/terminating) [53:6:0]
        Maxever session counts (estab/half-open/terminating) [53:18:3]
        Last session created 00:00:00
        Last statistic reset never
        Last session creation rate 115
        Maxever session creation rate 115
        Last half-open session total 6
        TCP reassembly statistics
        received 0 packets out-of-order; dropped 0
        peak memory usage 0 KB; current usage: 0 KB
        peak queue length 0
    Class-map: class-default (match-any)
      Match: any
      Drop
        0 packets, 0 bytes
```
On the Network Mangement block Only DHCP, SYSLOG, DNS, NefFlow and 192.168.12.0/24 (admin) traffic is allowed from outside-in

```bash
FW-MANAGEMENT-ZONE#sh policy-map type inspect zone-pair Outside-Inside-zone
policy exists on zp Outside-Inside-zone
  Zone-pair: Outside-Inside-zone

  Service-policy inspect : Outside-Inside-policy

    Class-map: Outside-Inside-class (match-all)
      Match: access-group name Outside-Inside-acl

   Inspect
        Packet inspection statistics [process switch:fast switch]
        udp packets: [24:0]

        Session creations since subsystem startup or last reset 14
        Current session counts (estab/half-open/terminating) [0:0:0]
        Maxever session counts (estab/half-open/terminating) [4:4:0]
        Last session created 00:16:12
        Last statistic reset never
        Last session creation rate 0
        Maxever session creation rate 6
        Last half-open session total 0
        TCP reassembly statistics
        received 0 packets out-of-order; dropped 0
        peak memory usage 0 KB; current usage: 0 KB
        peak queue length 0

FW-MANAGEMENT-ZONE#sh ip access-lists Outside-Inside-acl
Extended IP access list Outside-Inside-acl
    10 permit udp any host 192.168.20.254 eq snmptrap (14 matches)
    20 permit udp any host 192.168.20.254 eq syslog
    30 permit udp any host 192.168.20.254 eq bootps
    40 permit ip 192.168.12.0 0.0.0.255 192.168.20.0 0.0.0.255
    50 permit udp any host 192.168.20.254 eq domain
```

**Control plane Policing (CoPP)**

CoPP is a security feature that protects the control plane of a router from unnecessary or Denial-of-Service (DoS) traffic. 
It ensures routing stability, reachability, and packet delivery by providing filtering and rate-limiting capabilities for the control plane packets.

CoPP utilizes the MQC model similar to QOS in its implementation.
It allows for the classification, marking, and policing of traffic based on various criteria.
In the context of CoPP, the MQC model is used to define policies that control the traffic directed towards the control plane of the router or switch

Control plane traffic may be but not limited to Routing protcols, ICMP traffic, NAT, IPSec

In this topology, COPP is configured on core (OSPF, ICMP, SSH traffic) and Edge routers (BGP, ICMP and SSH traffic).

```bash
EDGE-ROUTER-1#sh policy-map control-plane
 Control Plane

  Service-policy input: CoPP-policy

    Class-map: ICMP-traffic-class (match-all)
      170 packets, 19260 bytes
      5 minute offered rate 2000 bps, drop rate 0000 bps
      Match: access-group name ICMP-traffic
      police:
          cir 8000 bps, bc 1500 bytes
        conformed 159 packets, 17962 bytes; actions:
          transmit
        exceeded 11 packets, 1298 bytes; actions:
          drop
        conformed 2000 bps, exceeded 0000 bps

    Class-map: Routing-Protocol-class (match-all)
      14 packets, 1017 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name Routing-Protocol-acl
      police:
          cir 128000 bps, bc 4000 bytes, be 4000 bytes
        conformed 14 packets, 1017 bytes; actions:
          transmit
        exceeded 0 packets, 0 bytes; actions:
          transmit
        violated 0 packets, 0 bytes; actions:
          transmit
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps
```

## NAT and Quality of Service
Branch Officies' routers are configured with NAT to have internet connection rather than having traffic backhauled to HQ.
However, Firewall and QoS polices are similar across the branch routers for a uniform Internet policy.

Scavenger traffic (torrents and leisure streaming platforms) is dropped.
Social media traffic is policed to 512Kbps.

```bash
BRANCH-A-ROUTER-1#sh policy-map interface e0/0.10
 Ethernet0/0.10 
  Service-policy input: Internet-Policy

    Class-map: Scavenger-class (match-any)  
      77 packets, 31359 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol netflix
        77 packets, 31359 bytes
        5 minute rate 0 bps
      Match: protocol bittorrent
        0 packets, 0 bytes
        5 minute rate 0 bps
      drop
    Class-map: Social-media-class (match-any)  
      1936 packets, 160233 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol facebook
        0 packets, 0 bytes
        5 minute rate 0 bps
      Match: protocol twitter
        1936 packets, 160233 bytes
        5 minute rate 0 bps
      Match: protocol instagram
        0 packets, 0 bytes
        5 minute rate 0 bps
      police:
          cir 512000 bps, bc 16000 bytes
        conformed 1936 packets, 160233 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          drop 
        conformed 0000 bps, exceeded 0000 bps
```

**mGRE tunnel OoS**

Per Tunnel QOS is implemented to give priority to voice traffic 10% bandwidth and 20% CBWFQ for network management traffic (SNMP, SYSLOG)

NHRP group configured '*NHRP-20MBPS*' for spokes with 20Mbps internet(tunnel interface) and '*NHRP-10MBPS*' for spokes with
10Mbps internet (tunnel interfaces)

This can be verified on the Hub router below for spoke BR-A1 at 20Mbps CIR:
```bash

DMVPN-HUB-ROUTER#sh policy-map multipoint 
 
Interface Tunnel10 <--> 44.67.28.6 

  Service-policy output: 20MBPS-Tunnel-Policy

    Class-map: class-default (match-any)  
      1596 packets, 179136 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: any 
      Queueing
      queue limit 2500 packets
      (queue depth/total drops/no-buffer drops) 0/0/0
      (pkts output/bytes output) 1596/285336
      shape (average) cir 20000000, bc 80000, be 80000
      target shape rate 20000000

      Service-policy : 20MBPS-child-policy

        queue stats for all priority classes:
          Queueing
          queue limit 250 packets
          (queue depth/total drops/no-buffer drops) 0/0/0
          (pkts output/bytes output) 0/0

        Class-map: Network-Management-class (match-any)  
          335 packets, 41206 bytes
          5 minute offered rate 0000 bps, drop rate 0000 bps
          Match: protocol snmp
            255 packets, 33014 bytes
            5 minute rate 0 bps
          Match: protocol syslog
            0 packets, 0 bytes
            5 minute rate 0 bps
          Match: protocol ssh
            80 packets, 8192 bytes
            5 minute rate 0 bps
          Match:  dscp cs2 (16)
            0 packets, 0 bytes
            5 minute rate 0 bps
          Queueing
          queue limit 500 packets
          (queue depth/total drops/no-buffer drops) 0/0/0
          (pkts output/bytes output) 335/64578
          bandwidth 20% (2000 kbps)
          
        Class-map: Voice-class (match-any)  
          0 packets, 0 bytes
          5 minute offered rate 0000 bps, drop rate 0000 bps
          Match: protocol rtp-audio
            0 packets, 0 bytes
            5 minute rate 0 bps
          Match:  dscp ef (46)
            0 packets, 0 bytes
            5 minute rate 0 bps
          Priority: 10% (1000 kbps), burst bytes 25000, b/w exceed drops: 0
```

## Network Monitoring
All Routers, Switches  are configured to send SNMP traps to the MGT server.
The MGT server uses PRTG to solicit information via SNMP for general network monitoring, NetFlow for traffic analysis, and Syslog for the capture and analysis of system log data.

On ISP-SW1 and ISP-SW2, we've set up RSPAN to capture VPN traffic and SPAN to capture internet-bound traffic. 
These configurations help monitor and secure the network. The captured data is sent to an Intrusion Detection System (IDS) for analysis. 
This approach enhances our ability to detect and address potential security issues in both VPN and internet traffic.
```bash
Sample RSPAN and SPAN config:
ISP-SWITCH-2#sh monitor session all
Session 1
---------
Type                     : Remote Destination Session
Source RSPAN VLAN      : 66
Destination Ports      : Et3/2
    Encapsulation      : Native


Session 2
---------
Type                     : Local Session
Source Ports             :
    Both                 : Et0/0
Destination Ports      : Et3/3
    Encapsulation      : Native

Sample SNMP config:
  snmp-server community device_snmp RO SNMP-SERVER
  snmp-server system-shutdown
  snmp-server enable traps config
  snmp-server host 192.168.20.254 version 2c device_snmp
```



## GNS3 Images used:
* Routers and IOS firewalls: [i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin](https://www.gns3.com/marketplace/appliances/cisco-iou-l3)
* Switches: i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
* SDN conroller: [Ubuntu VM](https://ubuntu.com/desktop)
* Windows server: [Windows_Server_2016_Datacenter_EVAL_en-us_14393_refresh](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2016)
* IDS: [Ostinato Wireshark](https://gns3.com/marketplace/appliances/ostinato-wireshark)
* Admin-PC: Windows 8.1 ISO VM
* End-user PCs: [Webterm Docker](https://gns3.com/marketplace/appliances/webterm)
