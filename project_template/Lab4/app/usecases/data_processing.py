from app.entities.data import Data
from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData
import time


def process_agent_data(data: Data) -> ProcessedAgentData:
    state = "good"
    if data.parking.empty_count >= 19:
        state = "bad"
    time.sleep(1)
    return ProcessedAgentData(road_state=state, agent_data=AgentData(
        accelerometer=data.accelerometer, gps=data.gps, timestamp=data.timestamp))
