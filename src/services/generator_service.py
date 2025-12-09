import logging
from typing import List, Optional
from src.domain.models import UserProfile, ProjectTemplate, GeneratedProject
from src.domain.enums import DifficultyLevel
from src.infra.repository import TemplateFileRepository

logger = logging.getLogger(__name__)

class ProjectGeneratorService: 
    """
    Core business logic service responsible for matching a user profile
    with the most suitable project templates.
    """
    def __init__(self, repository: TemplateFileRepository):
        """
        Dependency Injection: The service receives the repository instance.
        This makes testing easier (we can mock the repository).
        """
        self.repository = repository

    def generate_suggestion(self, user_profile: UserProfile) -> Optional[GeneratedProject]:
        """
        Main business method. It fetches templates and finds the best match.
        
        Args:
            user_profile (UserProfile): The input data from the user.
            
        Returns:
            GeneratedProject | None: The best matching project or None if no match found.
        """
        templates = self.repository.load_templates()

        if not templates:
            logger.warning("No templates avaible in repository.")
            return None
        
        best_match: Optional[GeneratedProject] = None
        highest_score = -1.0

        for template in templates:
            score, reasoning = self._calculate_compatibility(user_profile, template)

            #We filter out projects with 0 compatibility to ensure quality
            if score > highest_score and score > 0:
                highest_score = score
                best_match = GeneratedProject(
                    template=template,
                    compatibility_score=score,
                    reasoning=reasoning,
                )
                if best_match:
                    logger.info(f"Generated suggestion: {best_match.template.title} (Score: {highest_score})")
                else:
                    logger.info("No suitable project found for the given profile.")
                return best_match
        
    def _calculate_compatibility(self, user: UserProfile, template:ProjectTemplate) -> tuple[float, str]:
        """
        Internal helper method to score a template against a user profile.
        
        Algorithm Logic:
        1. Stack Match (Weight: 70%): How many user stacks overlap with template stacks?
        2. Level Match (Weight: 30%): Does the difficulty match?
        
        Returns:
            tuple[float, str]: The calculated score (0.0 to 1.0) and a reasoning string.
        """

        # 1. Normalize strings to lowercase for comparision to avoid "Python" != "python"
        user_stacks = {s.lower() for s in user.current_stacks}
        template_stacks = {s.lower() for s in template.recommended_stacks}

        # Calculate intersection (common stacks)
        common_stacks = user_stacks.intersection(template_stacks)

        if not template_stacks:
            stack_score = 0.0
        else:
            stack_score = len(common_stacks) / len(template_stacks)
        
        # 2. Difficulty Match
        level_score = 1.0 if user.experience_level == template.difficulty else 0.5

        # 3. Weighted Final Score
        final_score = (stack_score * 0.7) + (level_score * 0.3)

        #Create reasoning text
        if not common_stacks:
            reasoning = "Low match. This project requires stacks you might not know yet."
        else:
            stack_names = ", ".join([s.title() for s in common_stacks])
            reasoning = f"Great match! You already know: {stack_names}. The difficulty level is {template.difficulty.value}."
        
        return round(final_score, 2), reasoning