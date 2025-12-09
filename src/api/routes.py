from fastapi import APIRouter, Depends, HTTPException, status
from src.domain.models import UserProfile, GeneratedProject
from src.services.generator_service import ProjectGeneratorService
from src.infra.repository import TemplateFileRepository

# Create a router instance.
router = APIRouter()

def get_generator_service() -> ProjectGeneratorService:
    """
    Dependency Injection Factory.
    
    This function instantiates the necessary classes to build the Service.
    FastAPI calls this automatically when the endpoint is hit.
    
    If we switch to a Database later, we only change this function to use
    'TemplateDBRepository' instead of 'TemplateFileRepository'.
    """
    repository = TemplateFileRepository()
    return ProjectGeneratorService(repository)

@router.post(
    "/generate",
    response_model=GeneratedProject,
    status_code=status.HTTP_200_OK,
    summary="Generate a project idea based on user profile"
)
async def generate_project_idea(
    user_profile: UserProfile,
    service: ProjectGeneratorService = Depends(get_generator_service)
):
    """
    Endpoint to receive user stacks/level and return a project suggestion.
    
    - **user_profile**: JSON body containing stacks, level, and focus areas.
    - **Returns**: A GeneratedProject object with the template and compatibility score.
    """

    #Delegate business logic to the service layer
    result = service.generate_suggestion(user_profile)

    if not result:
        #if no project matches, we return a 404 (Not Found)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No suitable project template found for the given criteria."
        )
    return result