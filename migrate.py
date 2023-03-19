# Initializing database and table connections
import sqlalchemy

from app.configs.config import settings
from app.models.user import User
from app.models.trusted_contact import TrustedContact
from app.models.sos_request import SosRequest
from app.models.translocation_history import TranslocationHistory

print('Migration starts')

engine = sqlalchemy.create_engine(settings.db_url)

# Migration list
User.Meta.table.create(engine)
TrustedContact.Meta.table.create(engine)
SosRequest.Meta.table.create(engine)
TranslocationHistory.Meta.table.create(engine)

print('Migrated successfully')
