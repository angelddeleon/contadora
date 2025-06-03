"""actualizar_porcentaje_retencion

Revision ID: 60a164db2290
Revises: 70d1a4acfb72
Create Date: 2024-02-13 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = '60a164db2290'
down_revision = '70d1a4acfb72'
branch_labels = None
depends_on = None


def upgrade():
    # Actualizar el tipo de dato en retenciones_ventas
    op.execute('ALTER TABLE retenciones_ventas MODIFY COLUMN porcentaje_retencion FLOAT NOT NULL')
    
    # Actualizar el tipo de dato en retenciones_compras
    op.execute('ALTER TABLE retenciones_compras MODIFY COLUMN porcentaje_retencion FLOAT NOT NULL')


def downgrade():
    # Revertir cambios en retenciones_ventas
    op.execute("ALTER TABLE retenciones_ventas MODIFY COLUMN porcentaje_retencion ENUM('75', '100') NOT NULL")
    
    # Revertir cambios en retenciones_compras
    op.execute("ALTER TABLE retenciones_compras MODIFY COLUMN porcentaje_retencion ENUM('75', '100') NOT NULL")
