"""initial

Revision ID: 000000000000
Revises: 
Create Date: 2025-11-17 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '000000000000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # initial baseline; actual tables were created directly via create_tables.py
    pass


def downgrade():
    pass
