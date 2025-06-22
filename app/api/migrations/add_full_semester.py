from sqlalchemy import Column, Boolean
from app.api.database import Base, engine

def upgrade():
    # Добавляем новое поле is_full_semester в таблицу schedule_templates
    with engine.connect() as conn:
        conn.execute("""
            ALTER TABLE schedule_templates 
            ADD COLUMN is_full_semester BOOLEAN DEFAULT FALSE
        """)
        conn.commit()

def downgrade():
    # Удаляем поле is_full_semester из таблицы schedule_templates
    with engine.connect() as conn:
        conn.execute("""
            ALTER TABLE schedule_templates 
            DROP COLUMN is_full_semester
        """)
        conn.commit() 