"""cambiar porcentaje_retencion a float

Revision ID: a29c53456b4b
Revises: 
Create Date: 2025-06-02 23:34:37.171969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a29c53456b4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Modificar la tabla retenciones_ventas
    with op.batch_alter_table('retenciones_ventas', schema=None) as batch_op:
        batch_op.alter_column('porcentaje_retencion',
               existing_type=mysql.ENUM('75', '100', collation='utf8mb4_unicode_ci'),
               type_=sa.Float(),
               existing_nullable=False)

    # Modificar la tabla retenciones_compras
    with op.batch_alter_table('retenciones_compras', schema=None) as batch_op:
        batch_op.alter_column('porcentaje_retencion',
               existing_type=mysql.ENUM('75', '100', collation='utf8mb4_unicode_ci'),
               type_=sa.Float(),
               existing_nullable=False)


def downgrade():
    # Revertir cambios en retenciones_ventas
    with op.batch_alter_table('retenciones_ventas', schema=None) as batch_op:
        batch_op.alter_column('porcentaje_retencion',
               existing_type=sa.Float(),
               type_=mysql.ENUM('75', '100', collation='utf8mb4_unicode_ci'),
               existing_nullable=False)

    # Revertir cambios en retenciones_compras
    with op.batch_alter_table('retenciones_compras', schema=None) as batch_op:
        batch_op.alter_column('porcentaje_retencion',
               existing_type=sa.Float(),
               type_=mysql.ENUM('75', '100', collation='utf8mb4_unicode_ci'),
               existing_nullable=False)
