"""Static goals list endpoint."""

from fastapi import APIRouter

from models.schemas import GoalDefinition


router = APIRouter()


GOALS = [
    GoalDefinition(id="work",         label="Work",         description="Leadership, collaboration, and professional influence"),
    GoalDefinition(id="money",        label="Money",        description="Negotiation, deals, financial decisions"),
    GoalDefinition(id="relationship", label="Relationship", description="Connection, trust, and interpersonal dynamics"),
]


@router.get("", response_model=list[GoalDefinition])
def list_goals():
    return GOALS
