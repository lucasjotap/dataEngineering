import os
import boto3
import logging

from typing import NoReturn, List
from dataclasses import dataclass
from botocore.exceptions import ClientError

@dataclass
class StackDeployment(object):
	"""
	Classe StackDeployment lidará com a infraestrutura da criação de stacks junto com o CloudFormation.
	"""
	logging.getLogger().setLevel(logging.INFO)
	cloudformation_client = boto3.client('cloudformation')

	def create_stack(self, stack_name, template_body, **kwargs) -> NoReturn:
		"""Método para a criação de stacks."""
	    cloudformation_client.create_stack(
	        StackName=stack_name,
	        TemplateBody=template_body,
	        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
	        TimeoutInMinutes=30,
	        OnFailure='ROLLBACK'
	    )

	    cloudformation_client.get_waiter('stack_create_complete').wait(
	        StackName=stack_name,
	        WaiterConfig={'Delay': 5, 'MaxAttempts': 600}
	    )

	    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
	    logging.info(f'CREATE COMPLETE')


    def update_stack(self, stack_name, template_body, **kwargs) -> NoReturn:
    	"""Método para a atualização de stacks, se necessário."""
	    try:
	        cloudformation_client.update_stack(
	            StackName=stack_name,
	            Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
	            TemplateBody=template_body
	        )

	    except ClientError as e:
	        if 'No updates are to be performed' in str(e):
	            logging.info(f'SKIPPING UPDATE: No updates to be performed at stack {stack_name}')
	            return e

	    cloudformation_client.get_waiter('stack_update_complete').wait(
	        StackName=stack_name,
	        WaiterConfig={'Delay': 5, 'MaxAttempts': 600}
	    )

	    cloudformation_client.get_waiter('stack_exists').wait(StackName=stack_name)
	    logging.info(f'UPDATE COMPLETE')


    def get_existing_stacks(self) -> str:
    	"""
    	"""
	    response = cloudformation_client.list_stacks(
	        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
	    )

	    return [stack['StackName'] for stack in response['StackSummaries']]


	def _get_abs_path(self, path) -> str:
	    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


	def create_or_update_stack() -> NoReturn:
	    stack_name = 's3-bucket-ci'
	    with open(_get_abs_path('s3_bucket.yml')) as f:
	        template_body = f.read()

	    existing_stacks = self.get_existing_stacks()

	    if stack_name in existing_stacks:
	        logging.info(f'UPDATING STACK {stack_name}')
	        self.update_stack(stack_name, template_body)
	    else:
	        logging.info(f'CREATING STACK {stack_name}')
	        self.create_stack(stack_name, template_body)

if __name__ == "__main__":
	StackDeployment.create_or_update_stack()