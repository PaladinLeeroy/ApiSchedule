from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

# Base schemas for related models
class TeacherBase(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    id: int
    number: str
    capacity: int
    description: str | None = None

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    id: int
    name: str
    type: str
    description: str

    class Config:
        from_attributes = True

# Schedule Template schemas
class ScheduleTemplateBase(BaseModel):
    name: str
    date_start: date
    date_end: date
    group_type: str
    schedule_type: str
    is_full_semester: bool = False

class ScheduleTemplateCreate(ScheduleTemplateBase):
    pass

class ScheduleTemplateResponse(ScheduleTemplateBase):
    id: int

    class Config:
        from_attributes = True

# Schedule schemas
class ScheduleBase(BaseModel):
    template_id: int
    date: date
    group_id: int
    lesson_id: int
    teacher_id: int
    room_id: int
    lesson_number: int
    is_above_line: bool
    lesson_type: str
    day_of_week: Optional[int] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True

class LessonWithDetails(BaseModel):
    id: int
    name: str
    teacher: TeacherBase

    class Config:
        from_attributes = True

class ScheduleWithDetails(ScheduleResponse):
    lesson: LessonWithDetails
    teacher: TeacherBase
    room: RoomBase
    group: GroupBase
    template: ScheduleTemplateResponse

    class Config:
        from_attributes = True

# Group schemas
class GroupCreate(BaseModel):
    name: str
    type: str
    description: str

class GroupResponse(GroupBase):
    pass

# Teacher schemas
class TeacherCreate(BaseModel):
    name: str
    description: str

class TeacherResponse(TeacherBase):
    pass

# Room schemas
class RoomCreate(BaseModel):
    number: str
    capacity: int
    description: Optional[str] = None

class RoomResponse(RoomBase):
    pass

# Lesson schemas
class LessonBase(BaseModel):
    name: str
    teacher_id: int

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int

    class Config:
        from_attributes = True

class GroupDelete(BaseModel):
    id: int

class TeacherUpdate(BaseModel):
    name: str
    description: str

class LessonsCreate(BaseModel):
    name: str
    teacher: int

class LessonsUpdate(BaseModel):
    name: str
    teacher: int

class ScheduleItemCreate(BaseModel):
    date: date
    lesson_id: int
    teacher_id: int
    room: str
    lesson_number: int
    is_above_line: bool
    lesson_type: str

class ScheduleTemplateWithItems(BaseModel):
    template: ScheduleTemplateResponse
    items: List[ScheduleItemCreate]

class RoomUpdate(BaseModel):
    number: str | None = None
    capacity: int | None = None
    description: str | None = None

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Todo schemas
class TodoBase(BaseModel):
    text: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
