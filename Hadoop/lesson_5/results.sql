
SET silent=on; -- чтобы не получать дополнительную информацию

DROP DATABASE mydb CASCADE;
SHOW DATABASES;
CREATE DATABASE mydb; --hdfs dfs -du -h /user/hive/warehouse
SHOW DATABASES;
USE mydb;
SHOW TABLES;

-- Создаём первую таблицу "base" на основе файла
DROP TABLE if exists mydb.base;
CREATE EXTERNAL TABLE mydb.base (
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION "/testdata"
TBLPROPERTIES ("skip.header.line.COUNT"="1")
;
SELECT * FROM BASE LIMIT 10;
SHOW TBLPROPERTIES mydb.base;

-- Все остальные таблицы создаём и заполняем через insert из основной

-- TEXTFILE
DROP TABLE IF EXISTS mydb.txt;
CREATE TABLE mydb.txt
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
INSERT OVERWRITE TABLE mydb.txt SELECT * FROM base;

-- SequenceFile
DROP TABLE IF EXISTS mydb.sqf; 
CREATE TABLE mydb.sqf
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS SequenceFile;
INSERT OVERWRITE TABLE mydb.sqf SELECT * FROM base;

-- ORC UNCOMPRESSED
DROP TABLE IF EXISTS mydb.orc; 
CREATE TABLE mydb.orc
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS ORC
TBLPROPERTIES("orc.compress"="NONE");
INSERT OVERWRITE TABLE mydb.orc SELECT * FROM base;

-- ORC ZLIB
DROP TABLE IF EXISTS mydb.orc_zlib; 
CREATE TABLE mydb.orc_zlib
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS ORC
TBLPROPERTIES("orc.compress"="ZLIB");
INSERT OVERWRITE TABLE mydb.orc_zlib SELECT * FROM base;

-- AVRO
DROP TABLE IF EXISTS mydb.avro; 
CREATE TABLE mydb.avro
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS AVRO;
INSERT OVERWRITE TABLE mydb.avro SELECT * FROM base;

-- parquet UNCOMPRESSED
DROP TABLE IF EXISTS mydb.pq;
SET hive.exec.compress.output=false;
SET parquet.compression=UNCOMPRESSED;
CREATE TABLE mydb.pq
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS PARQUET;
INSERT OVERWRITE TABLE mydb.pq SELECT * FROM base;

-- parquet SNAPPY
DROP TABLE IF EXISTS mydb.pq_sn;
SET hive.exec.compress.output=true;
SET parquet.compression=SNAPPY;
CREATE TABLE mydb.pq_sn
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS PARQUET;
INSERT OVERWRITE TABLE mydb.pq_sn SELECT * FROM base;

-- parquet GZIP
DROP TABLE IF EXISTS mydb.pq_gz;
SET hive.exec.compress.output=true;
SET parquet.compression=GZIP;
CREATE TABLE mydb.pq_gz
(
Dispatching_base_num string,
Pickup_date timestamp,
Affiliated_base_num string,
locationID int
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS PARQUET;
INSERT OVERWRITE TABLE mydb.pq_gz SELECT * FROM base;


SET silent=false; -- чтобы получать скорость выполнения запросов

-- получаем скорость выполнения запросов
SELECT COUNT(*) FROM mydb.txt;  -- 0.081
SELECT COUNT(*) FROM mydb.txt;  -- 0.073
SELECT COUNT(*) FROM mydb.txt;  -- 0.068

SELECT COUNT(*) FROM mydb.pq;  -- 0.066
SELECT COUNT(*) FROM mydb.pq;  -- 0.06
SELECT COUNT(*) FROM mydb.pq;  -- 0.073

SELECT COUNT(*) FROM mydb.pq_sn;  -- 0.073
SELECT COUNT(*) FROM mydb.pq_sn;  -- 0.071
SELECT COUNT(*) FROM mydb.pq_sn;  -- 0.065

SELECT COUNT(*) FROM mydb.pq_gz;  -- 0.072
SELECT COUNT(*) FROM mydb.pq_gz;  -- 0.078
SELECT COUNT(*) FROM mydb.pq_gz;  -- 0.083

SELECT COUNT(*) FROM mydb.sqf;  -- 0.087
SELECT COUNT(*) FROM mydb.sqf;  -- 0.084
SELECT COUNT(*) FROM mydb.sqf;  -- 0.098

SELECT COUNT(*) FROM mydb.orc;  -- 0.082
SELECT COUNT(*) FROM mydb.orc;  -- 0.065
SELECT COUNT(*) FROM mydb.orc;  -- 0.085

SELECT COUNT(*) FROM mydb.orc_zlib;  -- 0.071
SELECT COUNT(*) FROM mydb.orc_zlib;  -- 0.096
SELECT COUNT(*) FROM mydb.orc_zlib;  -- 0.097

SELECT COUNT(*) FROM mydb.avro;  -- 0.091
SELECT COUNT(*) FROM mydb.avro;  -- 0.065
SELECT COUNT(*) FROM mydb.avro;  -- 0.073


SELECT COUNT(locationID) FROM mydb.txt;   -- 6.302
SELECT COUNT(locationID) FROM mydb.txt;   -- 6.295
SELECT COUNT(locationID) FROM mydb.txt;  -- 6.434

SELECT COUNT(locationID) FROM mydb.pq;  -- 4.346
SELECT COUNT(locationID) FROM mydb.pq;  -- 4.26
SELECT COUNT(locationID) FROM mydb.pq;  -- 4.259

SELECT COUNT(locationID) FROM mydb.pq_sn;  -- 4.298
SELECT COUNT(locationID) FROM mydb.pq_sn;  -- 4.267
SELECT COUNT(locationID) FROM mydb.pq_sn;  -- 4.288

SELECT COUNT(locationID) FROM mydb.pq_gz;  -- 4.263
SELECT COUNT(locationID) FROM mydb.pq_gz;  -- 4.255
SELECT COUNT(locationID) FROM mydb.pq_gz;  -- 4.267

SELECT COUNT(locationID) FROM mydb.sqf;  -- 24.284
SELECT COUNT(locationID) FROM mydb.sqf;  -- 23.342
SELECT COUNT(locationID) FROM mydb.sqf;  -- 22.5

SELECT COUNT(locationID) FROM mydb.orc;  -- 4.285
SELECT COUNT(locationID) FROM mydb.orc;  -- 4.27
SELECT COUNT(locationID) FROM mydb.orc;  -- 4.255

SELECT COUNT(locationID) FROM mydb.orc_zlib;  -- 4.259
SELECT COUNT(locationID) FROM mydb.orc_zlib;  -- 4.254
SELECT COUNT(locationID) FROM mydb.orc_zlib;  -- 4.302

SELECT COUNT(locationID) FROM mydb.avro;  -- 30.281
SELECT COUNT(locationID) FROM mydb.avro;  -- 28.278
SELECT COUNT(locationID) FROM mydb.avro;  -- 28.271


SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.txt;  -- 6.258
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.txt;  -- 6.253
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.txt;  -- 6.252

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq;  -- 4.257
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq;  -- 4.262
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq;  -- 4.252

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_sn;  -- 4.265
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_sn;  -- 4.254
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_sn;  -- 4.27

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_gz;  -- 4.327
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_gz;  -- 4.271
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.pq_gz;  -- 4.254

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.sqf;  -- 23.261
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.sqf;  -- 23.282
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.sqf;  -- 23.263

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc;  -- 4.29
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc;  -- 4.26
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc;  -- 4.257

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc_zlib;  -- 4.266
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc_zlib;  -- 4.248
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.orc_zlib;  -- 4.266

SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.avro;  -- 30.329
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.avro;  -- 30.3
SELECT COUNT(DISTINCT Dispatching_base_num) FROM mydb.avro;  -- 30.283

