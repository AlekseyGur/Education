
show databases;
show tables;

create database if not exists student41_35;

--зачем используем use?
use student41_35;
show tables;

drop table if exists student41_35.airport_codes;
drop table if exists student41_35.airport_codes_part;

create external table student41_35.airport_codes (
    id int,
    ident string,
    `type` string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_country string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
row format delimited fields terminated by ','
stored as TEXTFILE
location "/airports"
tblproperties ("skip.header.line.count"="1") --зачем нам эта опция?
;

drop table airport_codes;

select * from airport_codes limit 10; --почему пишем лимит?

--что делаем в этих запросах?
select count(distinct `type`) from airport_codes;
select distinct `type` from airport_codes;

drop table if exists student42_19.airport_codes_part;
;

show create table airport_codes_part
;
create table student42_19.airport_codes_part (
    id int,
    ident string,
    name string,
    latitude_deg string,
    longitude_deg string,
    elevation_ft string,
    continent string,
    iso_country string,
    iso_region string,
    municipality string,
    scheduled_service string,
    gps_code string, 
    iata_code string,
    local_code string,
    home_link string,
    wikipedia_link string,
    keywords string
)
partitioned by (`type` string)
stored as TEXTFILE
location '/user/student42_19/hive_test_loc'
;
set hive.exec.dynamic.partition.mode=nonstrict;
;
insert into table airport_codes_part 
partition(`type`)
select 
    id,ident,name,latitude_deg,longitude_deg,elevation_ft,
    continent,iso_country,iso_region,municipality,scheduled_service,
    gps_code,iata_code,local_code,home_link,wikipedia_link,keywords,
    `type`
from airport_codes
tablesample (1000 rows)
;
select * from airport_codes_part tablesample (10 rows) limit 10;
select count(distinct `type`) from airport_codes_part;
select distinct `type` from airport_codes_part;

MSCK REPAIR TABLE airport_codes_part;

/*
теперь посмотри в hive_test_loc через hdfs dfs -ls/-du и скажи, что заметил и почему там всё так
*/


--что такое temporary table и когда лучше использовать?
--что будет с содержимым таблицы, если колонки, по которым партиционируем, будут стоять не последними в селекте? 
create temporary table for_insert_airport_codes_part as
select 
     ident, `name`, elevation_ft, continent
    ,iso_region, municipality, gps_code, iata_code, local_code
    ,coordinates, iso_country, `type`
from student42_19.airport_codes t1
left join (
    select distinct
        `type` as type_2
    from student42_19.airport_codes_part
    ) t2 on t1.`type` = t2.type_2
where 
    t2.type_2 is null
;
select count(distinct `type`) from for_insert_airport_codes_part;
select distinct `type` from for_insert_airport_codes_part;
;
--чем insert overwrite отличается от insert into?
insert into student41_35.airport_codes_part partition(`type`)
select 
     ident, `name`, elevation_ft, continent
    ,iso_region, municipality, gps_code, iata_code, local_code
    ,coordinates, iso_country, `type`
from for_insert_airport_codes_part t1
limit 1000
;
select count(distinct `type`) from airport_codes_part;
select distinct `type` from airport_codes_part;

/*
STREAMING
выполни в баше это и скажи, что мы тут делаем:
    seq 0 9 > col_1 && seq 10 19 > col_2
    paste -d'|' col_1 col_2 | hdfs dfs -appendToFile - test_tab/test_tab.csv
*/
;
drop table if exists my_test_tab;
;
create temporary external table my_test_tab (
    col_1 int,
    col_2 int
)
row format delimited fields terminated by '|'
stored as TEXTFILE
location "/user/student41_35/test_tab"
;
select * from my_test_tab;
;

;
--что тут произошло и как это можно использовать ещё?
select
    transform(col_1, col_2) using "awk '{print $1+$2}'" as my_sum
from my_test_tab
;

-- /home/student41_35/mapred/mapper.py 
