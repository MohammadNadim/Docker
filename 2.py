import docker
from docker.errors import APIError
client = docker.from_env()

# make a list of network and get bridge network id
networkNameList = []
for network in client.networks.list():
	networkName = network.name
	networkNameList.append(networkName)
	if networkName == "bridge":
		bridgeNetworkID = network.id
	

CONTAINER = []  # store list of container
NETWORK = []    # store list of network
IP = []         # store list of ip address
NETID = []      # store list of network id
	

# create malicious network if it is not yet created
if "malicious" not in networkNameList:
		
	# configuration of malicious network
	ipam_pool = docker.types.IPAMPool(
		subnet = '172.30.0.0/16'
		)
	ipam_config = docker.types.IPAMConfig(
		pool_configs = [ipam_pool])

	# create new malicious network    
	client.networks.create("malicious", driver="bridge", check_duplicate = True, ipam = ipam_config)


# get all containers name, network, IP address, network id
for containerList in client.containers.list():
	containerName = containerList.name
	CONTAINER.append(containerName)
	#print containerName
	for key in containerList.attrs['NetworkSettings']['Networks']:
		containerNetworkName = key
		#print containerNetworkName
		NETWORK.append(containerNetworkName)
		
		containerIP = containerList.attrs['NetworkSettings']['Networks'][containerNetworkName]['IPAddress']
		#print containerIP
		IP.append(containerIP)
		
		containerNetworkID = containerList.attrs['NetworkSettings']['Networks'][containerNetworkName]['NetworkID']
		#print containerNetworkID
		NETID.append(containerNetworkID)
		

# main thing goes here		
count = 0
while count < len(IP):
	networkID = NETID[count]
	container = CONTAINER[count]
	ip = IP[count]
	malCont = 'maliciousContainer'
	malCont += str(count)
	containerNetwork = client.networks.get(networkID)
	containerNetwork.disconnect(container)
	client.containers.run('ubuntu',name = malCont, detach=True, tty=True, stdin_open=True)
	containerNetworkNew = client.networks.get(bridgeNetworkID)
	containerNetworkNew.disconnect(malCont)
	containerNew = client.containers.get(malCont)
	containerNetwork1 = client.networks.get(networkID)
	containerNetwork1.connect(malCont, ipv4_address = ip)
	count +=1
	
	
