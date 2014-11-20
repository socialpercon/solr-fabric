date >> start.txt
for((i=0;i<200;i++))
do
    core=`expr "$i" "%" "8"`
    java -Durl=http://192.168.0.173:8983/solr/core$core/update -Dtype=application/json -jar post.jar /home/logstash/snowdrop/snowdrop-load-example/sample1/perfomance_test/new200/2014*_$i.json >> log.txt &
    slp=`expr "$i" "%" "2"`
    if [ $slp == 0 ]
    then
        sleep 1
    fi
done
