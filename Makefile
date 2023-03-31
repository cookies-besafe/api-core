start:
	docker-compose up -d
up:
	docker-compose up
down:
	docker-compose down
stop:
	docker-compose stop
build:
	docker-compose build
migrate:
	docker exec -it python_container python3 migrate.py
enter_db:
	docker exec -it db_container psql --username=core_db_user --dbname=core_db
