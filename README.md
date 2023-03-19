# Getting started
```bash
cp .env.example .env
make build
make start
make migrate
```
## Port is 8008

### Migrations

After creating or changing model, you may run make migrate command to migrate tables, but it is very important to add new model if you made so into the migrate.py, like here
```python
User.Meta.table.create(engine)
```

### Location live update for the SOS button
- send POST /api/sos-request
- connect to the socket endpoint by WS/WSS /api/sos-request/{id\d+}/location-live-update
