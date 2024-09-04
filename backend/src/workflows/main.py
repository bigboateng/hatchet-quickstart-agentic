from .hatchet import hatchet
from .orchestrator_workflow import OrchestratorWorkflow
from .meeting_planning_workflow import MeetingPlanningAgentWorkflow
from .general_response_workflow import GeneralResponseAgentWorkflow

def start():
    worker = hatchet.worker("agent-worker")
    worker.register_workflow( GeneralResponseAgentWorkflow())
    worker.register_workflow( MeetingPlanningAgentWorkflow())
    worker.register_workflow(OrchestratorWorkflow())
    worker.start()
