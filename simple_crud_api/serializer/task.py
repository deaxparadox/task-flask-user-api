from dataclasses import dataclass


@dataclass
class TaskCreateSerializer():
    description: str
    body: str