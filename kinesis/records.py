import json
import boto3

from fake_web_events import Simulation #sionek's lib for running sims.

class Sim:
	"""
	Class for creating a simple simulation to record data with kinesis on AWS.
		- Methods: first_simulation, iterating_thru_records
	"""
	boto_object = None

	def first_simulation(self) -> dict:
		sim = Simulation(user_pool_size=500, sessions_per_day=1000)
		events: list = sim.run(duration_seconds=3) #json list.
		return events 

	def iterating_thru_records(self) -> None:
		events = self.first_simulation()
		Sim.boto_object = BotoClass() if Sim.boto_object is None else Sim.boto_object
		_ = list(map(Sim.boto_object.send_to_s3, events))


class BotoClass(object):
	"""
	Class will handle data serving to s3. 
	"""
	client = boto3.client('kinesis') #

	def send_to_s3(self, event):
		"""
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
	print(list(sim.first_simulation()))
