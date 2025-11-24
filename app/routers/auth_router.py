from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user_schemas import UserOut, Token
from app.models.user_models import User
from app.database.userdb import get_db
from app.utils.utils import hash_password, verify_password, create_access_token

router = APIRouter(tags=["auth"])


ALLOWED_ROLES = ["student", "teacher"]

@router.post("/register", response_model=UserOut)
async def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail=f"Role must be one of {ALLOWED_ROLES}")

    # Check if username exists
    result = await db.execute(select(User).filter_by(username=username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=username,
        hashed_password=hash_password(password),
        is_teacher=(role == "teacher")  # map role to boolean for database
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter_by(username=username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    role = "teacher" if db_user.is_teacher else "student"
    token_data = {"id": db_user.id, "role": role}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
