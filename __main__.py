import base64
import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

# [Placeholder 1: Create a private ECR registry.]
repo = aws.ecr.Repository('my-repo')

# [Placeholder 2: Get registry info (creds and endpoint).]
def getRegistryInfo(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])
image_name = repo.repository_url
registry_info = repo.registry_id.apply(getRegistryInfo)

image_name = repo.repository_url
registry_info = None # use ECR credentials helper.

# [Placeholder 3: Build and publish the container image.]
image = docker.Image('my-image',
    build='src/web',
    image_name=image_name,
    registry=registry_info,
)

pulumi.export('baseImageName', image.base_image_name)
pulumi.export('fullImageName', image.image_name)