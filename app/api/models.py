from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.api.database import Base
from datetime import datetime, date

class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String, index=True)
    description = Column(String, index=True)
    
    # Добавляем связь с расписанием
    schedules = relationship("Schedule", back_populates="group")

class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    # Добавляем связь с расписанием
    schedules = relationship("Schedule", back_populates="teacher")

class Lessons(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teachers")
    
    # Добавляем связь с расписанием
    schedules = relationship("Schedule", back_populates="lesson")

class ScheduleTemplate(Base):
    __tablename__ = "schedule_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    group_type = Column(String)  # Тип группы вместо ID
    date_start = Column(Date)
    date_end = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String, index=True)
    schedule_type = Column(String, default='regular')  # Добавляем тип расписания
    is_full_semester = Column(Boolean, default=False)  # Добавляем флаг для расписания на весь семестр
    
    # Добавляем связь с расписанием
    schedules = relationship("Schedule", back_populates="template")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    group_id = Column(Integer, ForeignKey("groups.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    lesson_number = Column(Integer)
    is_above_line = Column(Boolean, default=False)
    lesson_type = Column(String)
    template_id = Column(Integer, ForeignKey("schedule_templates.id"))
    day_of_week = Column(Integer)  # 1-6 для понедельника-субботы

    # Связи
    group = relationship("Groups", back_populates="schedules")
    lesson = relationship("Lessons", back_populates="schedules")
    teacher = relationship("Teachers", back_populates="schedules")
    room = relationship("Rooms", back_populates="schedules")
    template = relationship("ScheduleTemplate", back_populates="schedules")

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    capacity = Column(Integer)
    description = Column(String, index=True)
    
    # Добавляем связь с расписанием
    schedules = relationship("Schedule", back_populates="room")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # admin, teacher, student
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    todos = relationship("Todo", back_populates="user")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Связь с пользователем
    user = relationship("User", back_populates="todos")