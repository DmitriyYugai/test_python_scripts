CREATE TABLE book(
   uuid uuid PRIMARY KEY,
   name text,
   description text
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO book(uuid, name, description)
SELECT gen_random_uuid(),
        (select substr(md5((random()*generate_series)::text), 0, 25)),
        (select substr(md5((random()*generate_series)::text), 0, 25))
FROM generate_series(1, 100000);

DELETE FROM book;


SELECT uuid FROM book OFFSET 0 LIMIT 5000;

docker run -d \
	--name test_python_pg \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_PASSWORD=postgres \
	-e POSTGRES_DB=test_python \
	-v $HOME/DB_DATA/test_python_pg:/var/lib/postgresql/data \
	-p 5432:5432 \
	postgres:15.1
	
docker run -d \
	--name test_python_mongo \
	-e MONGO_INITDB_ROOT_USERNAME=mongo_user \
	-e MONGO_INITDB_ROOT_PASSWORD=mongo_pass \
	-e MONGO_INITDB_DATABASE=test_python \
	-v $HOME/DB_DATA/test_python_mongo:/data/db \
	-p 27017:27017 \
	mongo:6.0
