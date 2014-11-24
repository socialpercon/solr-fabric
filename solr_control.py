#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import sys

#Command

# 제대로 죽었는지 확인
@hosts(myhosts)
def shutdown_confirm():
    result = run("ps -ef | grep start")
    return result

@hosts(myhosts)
def run_case1():
    with cd("/home/logstash/solr-4.7.2/example"):
        run("java -Xms10240M -Xmx20480M -Dsolr.solr.home=multicore -Dcollection.configName=myconf -jar start.jar &", pty=False)

@hosts(case1_master_hosts)
def run_case1_master():
    result = run(command="cd /home/logstash/solr-4.7.0/example ; nohup java -Xms10240M -Xmx20480M -Dsolr.solr.home=solr -DzkRun -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -jar start.jar > output.log 2>&1 &", pty=False)
    return result
    
@hosts(case1_slave_hosts)
def run_case1_slave():
    result = run("cd /home/logstash/solr-4.7.0/example ; nohup java -Xms10240M -Xmx20480M -Djetty.port=8983 -DzkHost=192.168.0.171:9983 -jar start.jar > output.log 2>&1 &", pty=False)
    return result

@hosts(myhosts)
def delete_case1():
    result = run("rm -rf /home/logstash/solr-4.7.2/example/solr/collection1_*")
    return result

@hosts(case2_master_hosts)
def run_case2_master():
    result = run("cd /home/logstash/solr-4.7.0/cluster3 ; nohup java -Xms10240M -Xmx20480M -Dsolr.solr.home=solr -DzkRun -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -jar start.jar > output.log 2>&1 &", pty=False)
    return result

@hosts(case2_slave_hosts)
def run_case2_slave():
    front_host = env.host[:-1]
    host_num=env.host[-1:]
    back_host=str(int(host_num)-1)
    host = front_host+back_host
    print host
    
    cmd="cd /home/logstash/solr-4.7.0/cluster3 ; nohup java -Xms10240M -Xmx20480M -Djetty.port=8900 -DzkHost="+host+":9983 -jar start.jar > output.log 2>&1 &" 
    result = run(cmd, pty=False)
    return result

@hosts(case1_master_hosts)
#@parallel
def run_case3_master():
    result = run(command="cd /home/logstash/solr-4.7.0/multi_cluster3_1 ; nohup java -Xms10240M -Xmx20480M -Dsolr.solr.home=solr -Djetty.port=8983 -DzkRun=192.168.0.171:9983 -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -jar start.jar > output.log 2>&1 &", pty=False)
    result = run(command="cd /home/logstash/solr-4.7.0/multi_cluster3_2 ; nohup java -Xms10240M -Xmx20480M -Dsolr.solr.home=solr -Djetty.port=8984 -DzkRun=192.168.0.171:9984 -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -jar start.jar > output.log 2>&1 &", pty=False)
    result = run(command="cd /home/logstash/solr-4.7.0/multi_cluster3_3 ; nohup java -Xms10240M -Xmx20480M -Dsolr.solr.home=solr -Djetty.port=8985 -DzkRun=192.168.0.171:9985 -Dbootstrap_confdir=./solr/collection1/conf -Dcollection.configName=myconf -jar start.jar > output.log 2>&1 &", pty=False)
    return result

@hosts(case1_slave_hosts)
#@parallel
def run_case3_slave():
    result = run("cd /home/logstash/solr-4.7.0/multi_cluster3_1 ; nohup java -Xms10240M -Xmx20480M -Djetty.port=8983 -DzkHost=192.168.0.171:9983 -jar start.jar > output.log 2>&1 &", pty=False)
    result = run("cd /home/logstash/solr-4.7.0/multi_cluster3_2 ; nohup java -Xms10240M -Xmx20480M -Djetty.port=8984 -DzkHost=192.168.0.171:9984 -jar start.jar > output.log 2>&1 &", pty=False)
    result = run("cd /home/logstash/solr-4.7.0/multi_cluster3_3 ; nohup java -Xms10240M -Xmx20480M -Djetty.port=8985 -DzkHost=192.168.0.171:9985 -jar start.jar > output.log 2>&1 &", pty=False)
    return result

# elasticsearch로 실행된 모든 것을 죽임
@hosts(myhosts)
def kill_solr():
    put("./solr_kill.py", "~/" ,use_sudo=False);
    result = run("python ~/solr_kill.py")
    run("rm ~/solr_kill.py")
    return result

@hosts(myhosts)
def install():
    #put("./solr-4.7.2.tgz", "~/", use_sudo=False);
    #run("tar xzvf solr-4.7.2.tgz")
    with cd("/home/logstash/solr-4.7.2/example/multicore"):
        run("./run.sh")

@parallel
@hosts(myhosts)
def stat():
    run("top -b -n 1 -c -u logstash")
    run("vmstat")
    run("iostat")

# 노드에 인덱스 데이터 날리기 경로를 엄격하게 지정해줘야한다.
@hosts(myhosts)
def delete_case3_index():
    result = run("rm -rf ~/solr-4.7.0/multi_cluster3_1/solr/collection1_*")
    result = run("rm -rf ~/solr-4.7.0/multi_cluster3_2/solr/collection1_*")
    result = run("rm -rf ~/solr-4.7.0/multi_cluster3_3/solr/collection1_*")
    return result

# TEST CASE 3 elasticsearch 죽이기
def kill_elastic_test3():
    local("curl -XPOST '192.168.0.170:9200/_cluster/nodes/_shutdown'")
    local("curl -XPOST '192.168.0.170:9250/_cluster/nodes/_shutdown'")
    local("curl -XPOST '192.168.0.170:9150/_cluster/nodes/_shutdown'")
  
def sudo_java_run(command):
    sudo(command)

def merge_results(flag):
    if flag=="confirm":
        results = execute(shutdown_confirm)
    elif flag == "case1run":
        results = execute(run_case1_master)
        results = execute(run_case1_slave)
    elif flag == "case2run":
        results = execute(run_case2_master)
        results = execute(run_case2_slave)
    elif flag == "case3run":
        results = execute(run_case3_master)
        results = execute(run_case3_slave)
    elif flag == "delete":
        results = execute(delete_elastic_index)
    elif flag == "killall":
        results = execute(kill_solr)
    elif flag == "case3kill":
        results = execute(kill_elastic_test3)
    elif flag == "stat":
        results = execute(stat)

    print results
