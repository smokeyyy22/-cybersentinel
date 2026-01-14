from pydantic import BaseModel


class ThreatScenario(BaseModel):
    scenario: str


class ThreatAnalysis(BaseModel):
    case_id: str
    scenario: str
    threat_type: str
    severity: str
    analysis: str
    recommendations: list[str]
    context_sources: list[str]
    timestamp: str
    token_usage: int
