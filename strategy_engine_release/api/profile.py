"""Profile endpoints — replaces the v1 /api/onboarding endpoint.

  POST   /api/profile             create profile (first time)
  PUT    /api/profile             update profile (subsequent edits)
  GET    /api/profile             read raw profile
  GET    /api/profile/blueprint   read computed Energy Blueprint
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from models.orm import User, UserProfile
from models.schemas import (
    BirthChart, EnergyBlueprint, Pillar,
    ProfileCreate, ProfileRead,
)
from services.mbti import get_dominant_function, mbti_to_element
from services.saju import calculate_birth_chart


router = APIRouter()


def _to_blueprint(profile: UserProfile) -> EnergyBlueprint:
    """Assemble the static EnergyBlueprint from a stored profile."""
    chart = calculate_birth_chart(profile.birthdate, profile.birth_time)
    dominant_fn = get_dominant_function(profile.mbti)

    return EnergyBlueprint(
        mbti=profile.mbti,
        mbti_dominant_function=dominant_fn,
        mbti_element=mbti_to_element(profile.mbti),
        hd_type=profile.hd_type,
        birth_chart=BirthChart(
            day_master=chart["day_master"],
            pillars={k: Pillar(**v) for k, v in chart["pillars"].items()},
            element_counts=chart["element_counts"],
            dominant_elements=chart["dominant_elements"],
            weak_elements=chart["weak_elements"],
        ),
    )


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(
    req: ProfileCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileRead:
    if current.profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists. Use PUT /api/profile to update it.",
        )

    profile = UserProfile(
        user_id=current.id,
        birthdate=req.birthdate,
        birth_time=req.birth_time,
        birthplace=req.birthplace,
        mbti=req.mbti,
        hd_type=req.hd_type,
        personal_color=req.personal_color,
        blood_type=req.blood_type,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return ProfileRead.model_validate(profile)


@router.put("", response_model=ProfileRead)
def update_profile(
    req: ProfileCreate,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileRead:
    profile = current.profile
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile yet. Use POST /api/profile to create one.",
        )

    profile.birthdate      = req.birthdate
    profile.birth_time     = req.birth_time
    profile.birthplace     = req.birthplace
    profile.mbti           = req.mbti
    profile.hd_type        = req.hd_type
    profile.personal_color = req.personal_color
    profile.blood_type     = req.blood_type
    db.commit()
    db.refresh(profile)
    return ProfileRead.model_validate(profile)


@router.get("", response_model=ProfileRead)
def read_profile(current: User = Depends(get_current_user)) -> ProfileRead:
    if current.profile is None:
        raise HTTPException(status_code=404, detail="No profile yet.")
    return ProfileRead.model_validate(current.profile)


@router.get("/blueprint", response_model=EnergyBlueprint)
def read_blueprint(current: User = Depends(get_current_user)) -> EnergyBlueprint:
    if current.profile is None:
        raise HTTPException(status_code=404, detail="No profile yet.")
    return _to_blueprint(current.profile)
