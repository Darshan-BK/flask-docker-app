import docker

# Initialize Docker client
client = docker.from_env()

# List all active containers
containers = client.containers.list()
print("Active containers:")
for container in containers:
    print(f" - {container.name}: {container.status}")

# Check health of Flask container
flask_container = client.containers.get('flask-docker-app_web_1')
flask_status = flask_container.status
print(f"Flask container status: {flask_status}")

# Restart Flask container if unhealthy
if flask_status != 'running':
    print("Restarting Flask container...")
    flask_container.restart()
    print("Flask container restarted.")
