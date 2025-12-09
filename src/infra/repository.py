import json
import logging
from typing import List
from pathlib import Path
from src.domain.models import ProjectTemplate

# Initialize logger for this module
logger = logging.getLogger(__name__)

class TemplateFileRepository:
    """
    Infrastructure layer component responsible for accessing data 
    from the filesystem (templates.json).
    
    In Clean Architecture, this implementation acts as a 'Plugin' 
    to the domain. If we switch to a Database later, we just create 
    a 'TemplateDBRepository' and swap it.
    """

    def __init__(self, file_path: str = "src/templates/templates.json"):
        """
        Initializes the repository with the path to the JSON file.
        Using Path from pathlib ensures cross-platform compatibility (Windows/Linux/Mac).
        """
        self.file_path = Path(file_path)

    def load_templates(self) -> List[ProjectTemplate]:
        """
        Reads the JSON file and converts it into a list of Domain Entities (ProjectTemplate).
        
        Returns:
            List[ProjectTemplate]: A list of validated template objects.
        """
        try:
            if not self.file_path.exists():
                logger.error(f"Template file not found at: {self.file_path.absolute()}")
                return []

            with open(self.file_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Convert raw list of dicts into strict Pydantic models
            templates = [ProjectTemplate(**item) for item in data]
            
            logger.info(f"Successfully loaded {len(templates)} templates from file.")
            return templates

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading templates: {e}")
            return []