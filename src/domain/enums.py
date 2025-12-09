from enum import Enum

class DifficultyLevel(str, Enum):
    """
    Enumeration for project difficulty levels.
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class TechCategory(str, Enum):
    """
    Enumeration for technology categories to help filtering.
    """
    FRONTEND = "frontend"
    BACKEND = "backend"
    MOBILE = "mobile"
    DEVOPS = "devops"
    DATABASE = "database"