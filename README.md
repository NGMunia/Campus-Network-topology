
# Campus-Network-Topology

The following topology demonstrates a hierarchical network topology with a collapsed core while employing software defined networking (Automation).

The Branch networks are linked with a single-hub DMVPN for site to site VPN connectivity.
The network is also configures as BGP-AS-64511 as a non-transit Network, with ISPs only advertising a default route to the HQ site.





### Layer 2 connectivity:
The network Employs various layer 2 protocols namely:


**_LACP_**:

CORE switches and Access switches are configured with LACP in active-active mode.
Verification is seen below on the ACC-SW1:


``` bash
ACCESS-SWITCH-1#sh etherchannel summary
! Output omitted for brevity
Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP      Et1/0(P)    Et1/1(P)
2      Po2(SU)         LACP      Et1/2(P)    Et1/3(P)

```

**_Rapid PVST+ and Load balancing_**:

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


### Layer 3 connectivity:
The network Employs various layer 2 protocols namely:


**_InterVLAN Routing_**:

The network topology is designed as a collapsed core, where the core switches assume the responsibilities of both the core and distribution layers. 

One of the critical functions performed by these core switches is InterVLAN routing, enabling communication between different VLANs within the network.

To enhance network resilience and ensure continuous connectivity, HSRPv2 is implemented. HSRPv2 provides first hop redundancy by  ensuring a redundant and highly available network architecture.

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

**_Multi-Area OSPF_**:

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

**_EIGRP_**:

Within the network infrastructure, EIGRP is deployed to facilitate routing within mGRE tunnels, specifically configured under DMVPN architecture.

To enhance the efficiency of the network, spokes within the mGRE tunnels are optimized as stub routers. 
This minimizes the likelihood of Stuck-in-Active scenarios by preventing situations where EIGRP queries are sent but no acknowledgment is received.

Use of MD5 authentication, ensuring the integrity and authenticity of EIGRP messages exchanged within the mGRE tunnels. 

Bandwidth optimization feature is employed to enhance the utilization of available network resources within the mGRE tunnels.

```bash
Sample config:

BRANCH-A-ROUTER-2#sh running-config | s r e
router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface Tunnel20
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
  network 172.21.0.0 0.0.0.255
  metric weights 0 0 0 1 0 0 0
  eigrp stub connected summary
 exit-address-family
```


**_BGP_**:

Within the site's network architecture, BGP is implemented with a focus on non-transit site configuration for BGP NLRI. 
The design involves the propagation of only a default BGP route to the Campus network from the ISPs.
BGP peering is formed between EGDGE routers and their connected ISPs

To optimize the distribution of BGP traffic and ensure load-sharing, egress traffic is directed to exit through the Edge-1 router, by use of HSRPv2. 
To enable **automatic fail-over**, HSRP is configured in conjunction with IP-SLA and object tracking to track reachability of 44.67.28.1/32

On the other hand, Ingress traffic is routed through Edge-2. 
This is achieved by applying AS-prepending specifically to the prefix 32.19.86.0/27 when advertising it to the ISPs.

This AS-prepending technique involves adding multiple instances of the site's Autonomous System (AS) number to the AS-path attribute of the BGP route. 
In this scenario, it is applied to the prefix 32.19.86.0/27 outbound, influencing the inbound traffic flow through Edge-2.


```bash
router bgp 64511
 bgp log-neighbor-changes
 network 32.19.86.0 mask 255.255.255.224
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

**_Redistribution_**:

OSPF redistribution, Redistributes EIGRP spoke LAN prefixes into the OSPF domain.
EIGRP redistribution: Redistributes Specific Area 20 and VLAN 12 prefixes into EIGRP.
DMVPN-ROUTER is responsible for redistribution between OSPF and EIGRP domain.

```bash

BRANCH-A-ROUTER-1#sh ip route eigrp
      10.0.0.0/8 is variably subnetted, 6 subnets, 3 masks
D        10.1.10.0/23 is a summary, 02:25:31, Null0
D        10.1.20.0/23 [90/522240] via 172.20.0.3, 02:25:22, Tunnel10
D EX  192.168.12.0/24 [170/10240] via 172.20.0.1, 02:25:29, Tunnel10
D EX  192.168.20.0/24 [170/10240] via 172.20.0.1, 02:25:29, Tunnel10


FW-MANAGEMENT-ZONE#sh ip route ospf

O E2     10.1.10.0/23 [110/20] via 10.0.20.5, 02:26:20, Ethernet0/3
                      [110/20] via 10.0.20.1, 02:26:16, Ethernet0/2
O E2     10.1.20.0/23 [110/20] via 10.0.20.5, 02:26:10, Ethernet0/3
                      [110/20] via 10.0.20.1, 02:26:12, Ethernet0/2
```

### Automating the Network:
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
```

Sample code snippet of getting Network device **running configuration**:

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

### VPN Services:
DMVPN phase 2 with IPsec is used to secure communications between the HQ and the Branch spokes.
EIGRP is the protocol of choice for routing through the tunnels.

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

### Network Security:
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
On the Network Mangement clock Only DHCP,SYSLOG,DNS services and 192.168.12.0/24 (admin) prefix is allowed from outside-in

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
