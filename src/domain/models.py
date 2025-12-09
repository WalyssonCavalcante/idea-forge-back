from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from src.domain.enums import DifficultyLevel

class UserProfile(BaseModel):
    """
    Represents the input provided by the user seeking project ideas.
    """
    current_stacks: List[str] = Field(..., min_items=1, description="List of technologies the user works with")
    experience_level: DifficultyLevel
    focus_areas: List[str] = Field(default_factory=list, description="Areas intended for improvement")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_stacks": ["Python", "React", "FastAPI"],
                "experience_level": "intermediate",
                "focus_areas": ["Clean Architecture", "Unit Testing"]
            }
        }
    )

class ProjectTemplate(BaseModel):
    """
    Represents a static project template definition loaded from the system.
    """
    id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    recommended_stacks: List[str]
    features: List[str]
    learning_outcomes: List[str]

class GeneratedProject(BaseModel):
    """
    Represents the final output: A project suggestion tailored to the user.
    It combines the template with specific advice based on the user's stack.
    """
    template: ProjectTemplate
    compatibility_score: float # 0.0 to 1.0
    reasoning: str # Why this project was suggested
    
    def summary(self) -> str:
        """Returns a brief summary of the project generation."""
        return f"Project: {self.template.title} (Match: {int(self.compatibility_score * 100)}%)"