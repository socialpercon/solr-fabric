ps axf | grep "/home/logstash/snowdrop/thirdparty/java/bin/java -Dcom.sun.management.jmxremote.port=10001 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -Dsolr.solr.home=multicore -jar start.jar" | grep -v grep | awk '{print "kill -9 " $1}' | sh
ps axf | grep "java -Djetty.port=8984 -Dsolr.solr.home=multicore -jar start.jar" | grep -v grep | awk '{print "kill -9 " $1}' | sh


ls -al /DATA3/home/logstash/snowdrop/thirdparty/solr/example/multicore/default/syslog
rm -fr /DATA3/home/logstash/snowdrop/thirdparty/solr/example/multicore/default/syslog

#ls -al /DATA3/home/logstash/snowdrop/thirdparty/solr-4.10.2/example/multicore/default/syslog
#rm -fr /DATA3/home/logstash/snowdrop/thirdparty/solr-4.10.2/example/multicore/default/syslog
#cd /home/logstash/snowdrop/thirdparty/solr-4.9.0-copied/example
#java -Djetty.port=8984 -Dsolr.solr.home=multicore -jar start.jar >> /dev/null &
cd /home/logstash/snowdrop/thirdparty/solr/example
/home/logstash/snowdrop/thirdparty/java/bin/java -Dcom.sun.management.jmxremote.port=10001 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -Dsolr.solr.home=multicore -jar start.jar  >> /dev/null &

#cd /home/logstash/snowdrop/thirdparty/solr-4.10.2/example
#java -Djetty.port=8984 -Dsolr.solr.home=multicore -jar start.jar >> /dev/null &

