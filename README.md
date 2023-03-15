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