"""create specs/evaluations/rl_history tables

Revision ID: 85cc95e2c35b
Revises: 
Create Date: 2025-09-19 10:36:44.304198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85cc95e2c35b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create specs table
    op.create_table('specs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('spec_data', sa.JSON(), nullable=False),
        sa.Column('agent_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create evaluations table
    op.create_table('evals',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('spec_id', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('evaluation_data', sa.JSON(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['spec_id'], ['specs.id'])
    )
    
    # Create RL history table
    op.create_table('iteration_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('session_id', sa.String(), nullable=False),
        sa.Column('iteration_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create HIDG logs table
    op.create_table('hidg_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('day', sa.String(), nullable=False),
        sa.Column('task', sa.String(), nullable=False),
        sa.Column('values_reflection', sa.JSON(), nullable=False),
        sa.Column('achievements', sa.JSON(), nullable=True),
        sa.Column('technical_notes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create feedback logs table
    op.create_table('feedback_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('feedback_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('feedback_logs')
    op.drop_table('hidg_logs')
    op.drop_table('iteration_logs')
    op.drop_table('evals')
    op.drop_table('specs')
