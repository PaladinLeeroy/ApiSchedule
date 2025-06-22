"""add day_of_week to schedules

Revision ID: add_day_of_week_to_schedules
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_day_of_week_to_schedules'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('schedules', sa.Column('day_of_week', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('schedules', 'day_of_week') 