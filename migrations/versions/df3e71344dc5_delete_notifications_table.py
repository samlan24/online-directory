"""delete notifications table

Revision ID: df3e71344dc5
Revises: 5039dc24e812
Create Date: 2024-09-17 10:57:12.645813

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'df3e71344dc5'
down_revision = '5039dc24e812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('agent_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('message', mysql.TEXT(), nullable=False),
    sa.Column('read', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], name='notifications_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
