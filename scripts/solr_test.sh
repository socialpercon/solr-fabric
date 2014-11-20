ps axf | grep "/home/logstash/snowdrop/thirdparty/java/bin/java -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -Dsolr.solr.home=multicore -jar start.jar" | grep -v grep | awk '{print "kill -9 " $1}' | sh

for((i=0;i<200;i++))
do
    rm -r /home/logstash/solr-4.10.1/example/multicore/core$i/data
done

cd  /home/logstash/solr-4.10.1/example
/home/logstash/snowdrop/thirdparty/java/bin/java -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -Dsolr.solr.home=multicore -jar start.jar >> /dev/null &
cd -
