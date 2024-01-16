import docker
import logging
import os 
import base64 
import boto3 
from uuid import uuid4  

class HandlerEcr:

    def __init__(self):
        self.ENVIRONMENT = os.environ['ENVIRONMENT']
        self.AWS_REGION = os.environ['AWS_REGION']
        self.ECR_REPO_NAME = 'dev-crypto-extract-image'
        self.IMAGE_TAG = 'latest'
        self.docker_client = docker.from_env()

    def create_repository(self):
        client = boto3.client('ecr')

        try:
            client.create_repository(
                repositoryName=self.ECR_REPO_NAME,
                imageTagMutability='MUTABLE'
            )
        except client.exceptions.RepositoryAlreadyExistsException:
            logging.warning(f"Repository '{self.ECR_REPO_NAME}' already exists.")

    def _get_abs_path(self, path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

    def generate_hash(self, n):
        return str(uuid4().hex[:n])

    def connect_to_ecr(self):
        client = boto3.client('ecr')
        
        try:
            token = client.get_authorization_token()
        except Exception as e:
            logging.error(f"Error getting ECR authorization token: {e}")
            return None

        logging.info(f"CONNECTED TO ECR")

        b64token = token['authorizationData'][0]['authorizationToken'].encode('utf-8')
        username, password = base64.b64decode(b64token).decode('utf-8').split(':')
        registry = token['authorizationData'][0]['proxyEndpoint']

        try:
            self.docker_client.login(username=username, password=password, registry=registry, reauth=True)
        except docker.errors.APIError as e:
            logging.error(f"Error logging in to Docker registry: {e}")
            return None

        return registry

    def build_image(self):
        logging.info(f'BUILDING IMAGE: {self.ECR_REPO_NAME}:{self.IMAGE_TAG}')
        try:
            image, buildlog = self.docker_client.images.build(path=self._get_abs_path(''), rm=True, tag=f'{self.ECR_REPO_NAME}:{self.IMAGE_TAG}')
        except docker.errors.BuildError as e:
            logging.error(f"Error building Docker image: {e}")
            return None

        for log in buildlog:
            if log.get('stream'):
                logging.info(log.get('stream'))

        return image

    def tag_and_push_to_ecr(self, image, tag):
        self.create_repository()
        registry = self.connect_to_ecr()

        if registry is not None:
            logging.info(f"Pushing image to ECR: {self.ECR_REPO_NAME}:{tag}")
            ecr_repo_name = '{}/{}'.format(registry.replace('https://', ''), self.ECR_REPO_NAME)
            image.tag(ecr_repo_name, tag)

            try:
                push_log = self.docker_client.images.push(ecr_repo_name, tag=tag)
                logging.info(push_log)
            except docker.errors.APIError as e:
                logging.error(f"Error pushing Docker image to ECR: {e}")

    def update_image(self):
        image = self.build_image()

        if image is not None:
            self.tag_and_push_to_ecr(image, self.IMAGE_TAG)
            hash_tag = self.generate_hash(16)
            self.tag_and_push_to_ecr(image, hash_tag)
