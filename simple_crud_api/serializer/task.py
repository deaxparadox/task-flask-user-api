from dataclasses import dataclass


@dataclass
class TaskCreateSerializer:
    description: str
    body: str
    
# Employee task update
@dataclass
class TUESerializer:
    status: str
    
# Manager or team lead update
@dataclass
class TUMSerializer:
    status: str | None = None
    description: str | None = None
    body: str | None = None