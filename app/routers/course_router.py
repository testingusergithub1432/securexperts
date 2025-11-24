from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database.userdb import get_db
from app.models.user_models import Course, Enrollment
from app.schemas.user_schemas import CourseCreate, CourseOut, EnrollmentCreate, EnrollmentOut
from app.utils.utils import role_required

router = APIRouter(tags=["courses"])


@router.post("/courses", response_model=CourseOut)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(role_required(["teacher"
                                          ""]))
):
    new_course = Course(
        title=course.title,
        description=course.description,
        teacher_id=current_user.id
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@router.get("/courses", response_model=List[CourseOut])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@router.post("/enroll", response_model=EnrollmentOut)
async def enroll_in_course(
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(role_required(["student"]))
):
    new_enrollment = Enrollment(
        student_id=current_user.id,
        course_id=enrollment.course_id
    )
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    return new_enrollment
