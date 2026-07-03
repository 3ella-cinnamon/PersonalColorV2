"""Authentication endpoints: signup, login, current user."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from core.security import create_access_token, hash_password, verify_password
from models.orm import User
from models.schemas import CurrentUser, LoginResponse, ProfileRead, SignupRequest


router = APIRouter()


@router.post("/signup", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def signup(req: SignupRequest, db: Session = Depends(get_db)) -> LoginResponse:
    existing = db.query(User).filter(User.email == req.email).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists.",
        )

    user = User(email=req.email, password_hash=hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return LoginResponse(
        access_token=create_access_token(user.id),
        has_profile=False,
        profile=None,
    )


@router.post("/login", response_model=LoginResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    """OAuth2 password-flow login. `form.username` is the email.

    If the user already has a profile it is embedded in the response so
    the client does not need a separate GET /api/profile call.
    """
    user = db.query(User).filter(User.email == form.username).first()
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    profile = ProfileRead.model_validate(user.profile) if user.profile else None
    return LoginResponse(
        access_token=create_access_token(user.id),
        has_profile=profile is not None,
        profile=profile,
    )


@router.get("/me", response_model=CurrentUser)
def me(current: User = Depends(get_current_user)) -> CurrentUser:
    return CurrentUser(
        id=current.id,
        email=current.email,
        created_at=current.created_at,
        has_profile=current.profile is not None,
    )
