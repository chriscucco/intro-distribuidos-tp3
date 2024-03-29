# intro-distribuidos-tp3

## Mininet usage for custom topology

sudo mn --custom=mininet/custom/custom-topology.py --topo=custom,3,4 --mac --arp --switch=ovsk --controller=remote

where custom,x,y => x represent number of levels and y represents number of hosts


## Mininet usage for linear custom topology

sudo mn --custom=mininet/custom/linear-topology.py --topo=linearCustom,10 --mac --arp --switch=ovsk --controller=remote

where linearCustom,x => x represent number of switches. Hosts are 4, set by statement

## To not loose messages, must run the following command in mininetVM

sudo pox/pox.py samples.spanning_tree forwarding.l2_learning

## Firewall usage

The files to receive blocking and dropping rules, and the file to receive the switches where aply that rules, must be named blocking_rules.csv, dropping_rules.csv and switches_with_rules.csv respectively. This files must be dropped on pox folder (inside mininet VM enter: cd pox), against linear-topology-firewall.py.
The repository has one example for each .csv file. Notice that to aply a rule with more than one transport layer protocol, the line with the rul must be repeated as many times as protocols are to be applied. For example, if we want packets with destiny port 80 to be dropped, with tcp and udp, we must write on the .csv file:

id	linkProtocol	srcMac	dstMac	networkProtocol	srcIp	dstIp	transportProtocol	srcPort	  dstPort
1	ethernet			ipv4			tcp		80
2	ethernet			ipv4			udp		80





To run pox use the following command:
./pox.py forwarding.l2_learning linear-topology-firewall

For debugging run:
./pox.py log.level --DEBUG forwarding.l2_learning linear-topology-firewall

## Topology files

To create custom or linear topology with mininet must drop python files inside /mininet/custom.
