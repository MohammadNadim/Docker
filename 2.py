import docker
from docker.errors import APIError
client = docker.from_env()

# make a list of network
networkNameList = []
for network in client.networks.list():
	networkName = network.name
	networkNameList.insert(0,networkName)
	

CONTAINER = []
NETWORK = []
IP = []
NETID = []
	
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





# get all container name, network, IP address
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
		
		
# disconnect the containers from network		
count = 0
while count < len(IP):
	networkID = NETID[count]
	container = CONTAINER[count]
	ip = IP[count]
	malCont = 'maliciousContainer'
	malCont += str(count)
	containerNetwork = client.networks.get(networkID)
	containerNetwork.disconnect(container)
	client.containers.create('ubuntu',name = malCont)
	containerNetwork.connect(malCont, ipv4_address = ip)
	count +=1
	












