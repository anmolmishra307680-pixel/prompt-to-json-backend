"""Initial schema

Revision ID: 001
Create Date: 2024-01-17 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None

def upgrade():
    op.create_table('specs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('spec_data', sa.JSON(), nullable=False),
        sa.Column('agent_type', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('specs')