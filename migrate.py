# Initializing database and table connections
import sqlalchemy

from app.configs.config import settings
from app.models.user import User

print('Migration starts')

engine = sqlalchemy.create_engine(settings.db_url)

# Migration list
User.Meta.table.create(engine)

print('Migrated successfully')
