for((i=0;i<200;i++))
do
    slp=`expr "$i" "%" "3"`
    cp /home/logstash/snowdrop/snowdrop-load-example/sample1/perfomance_test/_source200/2014*_$i.json /home/logstash/snowdrop/snowdrop-load-example/sample1/perfomance_test/_source200.3.$slp/
done
