import docker

# Initialize Docker client
client = docker.from_env()

# Create a custom bridge network
network_name = 'flask-network'
try:
    network = client.networks.create(network_name, driver='bridge')
    print(f"Network '{network_name}' created.")
except docker.errors.APIError as e:
    print(f"Network '{network_name}' already exists.")

# List all networks
networks = client.networks.list()
for net in networks:
    print(net.name)

# Connect the Flask container and database container to the network
web_container = client.containers.get('flask-docker-app_web_1')
db_container = client.containers.get('flask-docker-app_mongo_1')
network.connect(web_container)
network.connect(db_container)

print(f"Containers connected to '{network_name}' network.")
