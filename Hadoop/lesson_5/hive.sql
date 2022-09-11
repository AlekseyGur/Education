



show databases;

select 1;

--Dispatching_base_num,Pickup_date,Affiliated_base_num,locationID
--B02617,2015-05-17 09:47:00,B02617,141
--B02617,2015-05-17 09:47:00,B02617,65
--B02617,2015-05-17 09:47:00,B02617,100
--B02617,2015-05-17 09:47:00,B02774,80
;
create database mydb; --hdfs dfs -du -h /user/hive/warehouse

show databases;

use mydb;

show tables;

drop table if exists mydb.uber_data_ex;

create external table uber_data_ex (
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
row format delimited fields terminated by ','
stored as TEXTFILE
location "/testdata"
tblproperties ("skip.header.line.count"="1")
--SERDEPROPERTIES("timestamp.formats"="yyyy-MM-dd HH:mm:ss")
;
SELECT * from uber_data_ex limit 10;
-- hdfs dfs -du -h /mydataset
select count(*) from uber_data_ex; --
select 
	count(distinct dispatching_base_num) 
from uber_data_ex; --
;


--set parquet.compression=UNCOMPRESSED/GZIP/SNAPPY
--CSV
create table uber_data_ex_csv
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
row format delimited fields  terminated by ","
stored as textfile;

insert overwrite table uber_data_ex_csv
select * from uber_data_ex
;
select * from uber_data_ex_csv limit 10;
;
select count(1) from uber_data_ex_csv; --засечь время
select count(locationID) from uber_data_ex_csv; --засечь время
select count(distinct dispatching_base_num) from uber_data_ex_csv; --засечь время


create table uber_data_ex_sq
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as sequencefile
;
insert overwrite table uber_data_ex_sq
select * from uber_data_ex
;
-- если интересно, что это за формат, сделайте hdfs dfs -cat в получившийся файл
select * from uber_data_ex_sq limit 10;
;
select count(1) from uber_data_ex_sq; --засечь время
select count(locationID) from uber_data_ex_sq; --засечь время
select count(distinct dispatching_base_num) from uber_data_ex_sq; --засечь время

--PARQUET
create table uber_data_ex_pq
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as parquet
;
insert overwrite table uber_data_ex_pq
select * from uber_data_ex
;
select count(1) from uber_data_ex_pq; --засечь время
select count(distinct locationID) from uber_data_ex_pq; --засечь время
select count(distinct dispatching_base_num) from uber_data_ex_pq; --засечь время

--ORC
create table uber_data_ex_orc
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as orc
;
insert overwrite table uber_data_ex_orc
select * from uber_data_ex
;
select count(1) from uber_data_ex_orc; --засечь время
select count(distinct dispatching_base_num) from uber_data_ex_orc; --засечь время

drop database mydb cascade;


--AVRO
create table uber_data_ex_avro
	(
	Dispatching_base_num string,
	Pickup_date timestamp,
	Affiliated_base_num string,
	locationID int
)
stored as avro
;
insert overwrite table uber_data_ex_avro
select * from uber_data_ex
;
show 

;
select * from uber_data_ex_avro limit 10;
;
select count(1) from uber_data_ex_avro; --засечь время
select count(locationID) from uber_data_ex_avro; --засечь время
select count(distinct dispatching_base_num) from uber_data_ex_avro;

drop database mydb cascade;




