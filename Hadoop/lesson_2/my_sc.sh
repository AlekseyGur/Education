#!/bin/bash

# 1. 2.
mkdir ~/lesson_2
cd ~/lesson_2
echo 'Hello,' > test_file_1
echo 'hdfs' > test_file_2
echo '!' > test_file_3
# 3. 
hdfs dfs -put -f test_file_1
hdfs dfs -put -f test_file_2
hdfs dfs -put -f test_file_3
hdfs dfs -setrep 2 test_file_*
hdfs dfs -cat test_file_* | awk '{print strftime("%Y-%m-%d %H:%M:%S"), $0;}' | hadoop fs -appendToFile - log.txt
hdfs dfs -cat log.txt
# 4.
hdfs dfs -mkdir task_2
hdfs dfs -mv test_file_* task_2/
# 5.
hdfs dfs -du task_2/* | awk '{print $2, $3;}'
# 6.
hdfs dfs -rm -r -skipTrash task_2
hdfs dfs -rm -r -skipTrash log.txt
rm -rf ~/lesson_2
