"""Initial migration

Revision ID: initial
Revises:
Create Date: 2023-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables
    op.create_table('tariffs',
                    sa.Column('id_market', sa.Integer(), nullable=False),
                    sa.Column('cdi', sa.Integer(), nullable=False),
                    sa.Column('voltage_level', sa.Integer(), nullable=False),
                    sa.Column('G', sa.Float(), nullable=True),
                    sa.Column('T', sa.Float(), nullable=True),
                    sa.Column('D', sa.Float(), nullable=True),
                    sa.Column('R', sa.Float(), nullable=True),
                    sa.Column('C', sa.Float(), nullable=True),
                    sa.Column('P', sa.Float(), nullable=True),
                    sa.Column('CU', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id_market', 'cdi', 'voltage_level')
                    )

    op.create_table('services',
                    sa.Column('id_service', sa.Integer(), nullable=False),
                    sa.Column('id_market', sa.Integer(), nullable=True),
                    sa.Column('cir', sa.Integer(), nullable=True),
                    sa.Column('voltage_level', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id_service')
                    )

    op.create_table('xm_data_hourly_per_agent',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('record_timestamp', sa.DateTime(), nullable=True),
                    sa.Column('value', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('records',
                    sa.Column('id_record', sa.Integer(), nullable=False),
                    sa.Column('id_service', sa.Integer(), nullable=True),
                    sa.Column('record_timestamp', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['id_service'], ['services.id_service'], ),
                    sa.PrimaryKeyConstraint('id_record')
                    )

    op.create_table('consumption',
                    sa.Column('id_record', sa.Integer(), nullable=False),
                    sa.Column('value', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['id_record'], ['records.id_record'], ),
                    sa.PrimaryKeyConstraint('id_record')
                    )

    op.create_table('injection',
                    sa.Column('id_record', sa.Integer(), nullable=False),
                    sa.Column('value', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['id_record'], ['records.id_record'], ),
                    sa.PrimaryKeyConstraint('id_record')
                    )

    # Create indexes
    op.create_index(op.f('ix_records_id_record'), 'records', ['id_record'], unique=False)
    op.create_index(op.f('ix_services_id_service'), 'services', ['id_service'], unique=False)


def downgrade():
    # Drop tables
    op.drop_index(op.f('ix_services_id_service'), table_name='services')
    op.drop_index(op.f('ix_records_id_record'), table_name='records')
    op.drop_table('injection')
    op.drop_table('consumption')
    op.drop_table('records')
    op.drop_table('xm_data_hourly_per_agent')
    op.drop_table('services')
    op.drop_table('tariffs')