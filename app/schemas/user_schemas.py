from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str
    is_teacher: bool = False

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    title: str
    description: Optional[str]

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    teacher_id: int
    model_config = ConfigDict(from_attributes=True)



class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int
    student_id: int
    progress: int
    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str
