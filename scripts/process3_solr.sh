#!/bin/bash
for((i=1;i<11;i++))
do
    fab -f multi_run_solr.py multi_merge_results:num=6
    #fab -f multi_run_solr.py merge_results:num=9
done
#for((i=1;i<11;i++))
#do
#    curl -XDELETE '192.168.0.170:9200/jetsetter'
#    sleep 5
#    fab -f multi_run.py merge_results:num=3
#done
#rm test_process-3.txt
#touch test_process-3.txt
#for((i=1;i<11;i++))
#do
#    curl -XDELETE '192.168.0.170:9200/jetsetter'
#    fab -f multi_run.py merge_results:num=3 >> test_process-3.txt
#done
