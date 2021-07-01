# intro-distribuidos-tp3

## Mininet usage for custom topology

sudo mn --custom=mininet/custom/custom-topology.py --topo=custom,3,4 --mac --arp --switch=ovsk --controller=remote

where custom,x,y => x represent number of levels and y represents number of hosts


## Mininet usage for linear custom topology

sudo mn --custom=mininet/custom/linear-topology.py --topo=linearCustom,10 --mac --arp --switch=ovsk --controller=remote

where linearCustom,x => x represent number of switches. Hosts are 4, set by statement

## To not loose messages, must run the following command in mininetVM

pox/pox.py samples.spanning_tree