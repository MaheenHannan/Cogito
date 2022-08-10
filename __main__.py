import base64
import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

repo = aws.ecr.Repository('my-repo')

def getRegistryInfo(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])
image_name = repo.repository_url
registry_info = repo.registry_id.apply(getRegistryInfo)

image = docker.Image('my-image',
    build='src/web',
    image_name=image_name,
    registry=registry_info,
)

# Export the base and specific version image name.
pulumi.export('baseImageName', image.base_image_name)
pulumi.export('fullImageName', image.image_name)