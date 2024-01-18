import json
import boto3

from fake_web_events import Simulation #sionek's lib for running sims.
from typing import List, Dict 
	
class Sim:
	"""
	Class for creating a simple simulation to record data with kinesis on AWS.
		- Methods: first_simulation, iterating_thru_records
	"""
	boto_object = None

	def first_simulation(self) -> dict:
		sim = Simulation(user_pool_size=500, sessions_per_day=1000)
		events: List[Dict] = sim.run(duration_seconds=3)
		return events 

	def iterating_thru_records(self) -> None:
		events: List[Dict] = self.first_simulation()
		Sim.boto_object = BotoClass() if Sim.boto_object is None else Sim.boto_object
		_: List = list(map(Sim.boto_object.send_to_s3, events))


class BotoClass(object):
	"""
	Class will handle data serving to s3. 
	"""
	client = boto3.client('firehose') #

	def send_to_s3(self, event):
		"""
		Method sends events to kinesis.
		"""
		data = json.dumps(event).encode('utf-8') # Transforming to string and encoding in utf-8
		response = BotoClass.client.put_record(
			StreamName = "kinesis-stream",
			Data = data,
			PartitionKey = "test"
		)
		return response

if __name__ == "__main__":
	sim: object = Sim()
	sim.iterating_thru_records()
