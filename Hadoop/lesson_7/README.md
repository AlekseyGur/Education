# Урок 8. Хранилища данных

## Задачи

- Развернуть касандру с репы docker-cassandra с ветки bde-cassandra (или на учебном кластере просто подключиться)
- Подключить к Cassandra
- Создать таблицы
- Вставить записи
- Изучить особенности работы where
- Cоздать таблицу с несколькими primary key, вставить значения, пофильтровать по ним (как по 1му, так и по 2м)
- Изучить особенности хранения данных

## Решение

``` SQL
docker-compose up -d

cqlsh 

describe keyspaces;
SELECT * FROM system.schema_keyspaces;

SELECT columnfamily_name FROM system.schema_columnfamilies WHERE keyspace_name = 'system_auth';

select columnfamily_name from system.schema_columnfamilies limit 1;

CREATE KEYSPACE if not exists lesson7 
   WITH REPLICATION = { 
      'class' : 'SimpleStrategy', 'replication_factor' : 1 
      }
;

CREATE TABLE if not exists lesson7.animals (
    id int, 
    name text,
    size text,
    --
    primary key (id)
)
;

CREATE COLUMNFAMILY if not exists animals (
    id int primary key, 
    name text,
    size text
    --
)
;


use lesson7;

insert into animals (id, name, size)
values (3, 'Deer', 'Big')
;
select * from animals;

insert into animals (id, name, size)
values (3, 'Bug', 'Small')
;

insert into animals (id, name, size)
values (5, 'Bee', 'Small')
;
insert into animals (id, name, size)
values (7, 'Bug', 'Big')
;



insert into animals_2 (id, name, size)
values (5, 'Bee', 'Small')
;
insert into animals (id, name, size)
values (7, 'Bug', 'Big')
;



Р›РѕРІРёРј РѕС€РёР±РєСѓ:
select * from animals
where id = 3 and name = '12321';

delete from animals where id = 3;

;
CREATE TABLE if not exists lesson7.animals_2 (
    id int, 
    name text,
    size text,
    --
    primary key (id, name)
)
;
;
select * from animals
where id = 2;

insert into animals (id, name, size)
values (3, null, null);

insert into animals (id, name, size)
values (null, null, null);

insert into animals (id, name, size)
values (4, null, null);

select * from animals
where id > 2;

SELECT * FROM animals WHERE TOKEN(id) > TOKEN(2);

CREATE TABLE if not exists lesson7.animals_2 (
    id_1 int,
    id_2 int, 
    name text,
    size text,
    --
    primary key (id_1, id_2)
)
;
insert into animals_2 (id_1, id_2, name, size)
values (2, 3, 'Bug', 'Small')
;
insert into animals_2 (id_1, id_2, name, size)
values (5, 7, 'Bug', 'Small')
;
insert into animals_2 (id_1, id_2, name, size)
values (5, 9, 'Deer', 'Big')
;

***HBASE***

docker-compose -f docker-compose-standalone.yml up -d


hbase shell

list_namespace

drop_namespace 'lesson7'

create_namespace 'lesson7'

create 'lesson7:animals', 'name', 'size'

list_namespace_tables 'lesson7'

describe 'lesson7:animals'

put 'lesson7:animals', '3', 'name', 'Deer'
put 'lesson7:animals', '3', 'size', 'Mid'

put 'lesson7:animals', '3', 'name', 'Dog'

alter 'lesson7:animals', {NAME => 'name', VERSIONS => 4}

put 'lesson7:animals', '5', 'name', 'Snake'
put 'lesson7:animals', '5', 'name', 'Pig'
put 'lesson7:animals', '5', 'size', 'Mid'

get 'lesson7:animals', '5', {COLUMN => 'name', VERSIONS => 4}

get  'lesson7:animals', '5'

scan 'lesson7:animals'
scan 'lesson7:animals', {LIMIT => 1}

count 'lesson7:animals'
count 'lesson7:animals', { INTERVAL => 1 }

deleteall 'lesson7:animals', '5'
get  'lesson7:animals', '5'

disable 'lesson7:animals'
drop 'lesson7:animals'
```
