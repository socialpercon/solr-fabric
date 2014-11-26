#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import re
import time
import threading
import Queue
from fabric.network import disconnect_all

env.parallel = True
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175','logstash@192.168.0.176']
my_hosts = ['logstash@192.168.0.170']
#master_hosts = ['logstash@192.168.0.171','logstash@192.168.0.173','logstash@192.168.0.175']
master_hosts = ['logstash@192.168.0.170']
slave_hosts = ['logstash@192.168.0.172','logstash@192.168.0.174''logstash@192.168.0.176']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171']
env.password = ''

#Command
command = "java -Durl=http://localhost:8983/solr/collection1/update -Dtype=text/json -jar post.jar"
file_directory = "~/solr-4.7.2/example/exampledocs"

#Java
jar_name = 'cluster.sh'
jar_path = "./" + jar_name

#Docs
docs_path = '../../data/json_data/'

@parallel
@hosts(master_hosts)
def delete_collection():
    run("curl -XGET 'http://localhost:8983/solr/admin/collections?action=DELETE&name=collection1'", pty=False)

@parallel
@hosts(my_hosts)
def delete_core(num):
    for i in xrange(0,int(num)):
        run("curl http://localhost:8983/solr/core%d/update -H 'Content-type: text/xml' --data-binary '<delete><query>*:*</query></delete>'" % (i))
        run("curl http://localhost:8983/solr/core%d/update -H 'Content-type: text/xml' --data-binary '<commit />'" % (i))
        run("curl http://localhost:8983/solr/core%d/update -H 'Content-type: text/xml' --data-binary '<optimize />'" % (i))
        run("curl -XGET 'http://localhost:8983/solr/admin/cores?action=UNLOAD&core=core%d&deleteindex=true'" % (i))

@parallel
@hosts(my_hosts)
def create_core(num):
    for i in xrange(0,int(num)):
        run("curl -XGET 'http://localhost:8983/solr/admin/cores?action=CREATE&name=core%s'" % (i))

@parallel
@hosts(master_hosts)
def init_data():
    run("curl 'http://localhost:8983/solr/admin/collections?action=CREATE&name=collection1&numShards=12&maxShardsPerNode=100&replicationFactor=1&collection.configName=myconf'", pty=False)

@parallel
@hosts(master_hosts)
def delete_data():
    run("curl -XGET 'http://localhost:8983/solr/admin/collections?action=DELETE&name=collection1'", pty=False)

#    run("curl -XGET 'http://localhost:8984/solr/admin/collections?action=DELETE&name=collection1'", pty=False)
#    run("curl -XGET 'http://localhost:8985/solr/admin/collections?action=DELETE&name=collection1'", pty=False)

#@parallel
#@hosts(master_hosts)
#def init_data():
#    run("curl 'http://localhost:8983/solr/admin/collections?action=CREATE&name=collection1&numShards=6&maxShardsPerNode=100&replicationFactor=2&collection.configName=myconf'", pty=False)
#    run("curl 'http://localhost:8984/solr/admin/collections?action=CREATE&name=collection1&numShards=6&maxShardsPerNode=100&replicationFactor=2&collection.configName=myconf'", pty=False)
#    run("curl 'http://localhost:8985/solr/admin/collections?action=CREATE&name=collection1&numShards=6&maxShardsPerNode=100&replicationFactor=2&collection.configName=myconf'", pty=False)

@parallel
@hosts(my_hosts)
def java_run(i):
    with cd(file_directory):
        #result = run("java -Durl=http://localhost:8983/solr/core%s/update -Dtype=text/json -jar post.jar %s-%d.json" % (i, env.host, i), pty=False)
        result = run("java -Durl=http://localhost:8983/solr/collection1/update -Dtype=text/json -jar post.jar %s-%d.json" % (env.host, i), pty=False)
    print result
    return result

@parallel
@hosts(master_hosts)
def multi_java_run(port, i):
    with cd(file_directory):
        result = run("java -Durl=http://localhost:%s/solr/collection1/update -Dtype=text/json -jar post.jar %s-%d.json" % (port, env.host, i), pty=False)
    return result

@parallel
@hosts(my_hosts)
def file_put(number):
    global command
    global file_directory
    
	# file
    run('mkdir -p ' + file_directory)
    put(jar_path, file_directory ,use_sudo=False);

    for i in xrange(1,int(number)+1):
        put("%s%s-%d.json" % (docs_path,env.host, i), file_directory, use_sudo=False);

def sudo_java_run(command):
    sudo(command)

def merge_results_with_file(num):
    execute(file_put, number=int(num))
    merge_results(num)

def merge_results(num):
    execute(delete_data)
    execute(init_data)
    #time.sleep(2)
    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(0,int(num)):
        t = ExecThread(i, queue)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    timeregex = re.compile('.*\s.*\s.*\s.*\s.*\sTime spent: 0:00:(.*)')
    timestamps = []
    for message in messages:
        for result in message.itervalues():
            match = timeregex.match(result).group(1)
            timestamps.append(float(match))

    print timestamps
    print "avg : %f" % (sum(timestamps,0.0)/len(timestamps))

def multi_merge_results(num):
    execute(delete_data)
    time.sleep(2)
    execute(init_data)
    time.sleep(3)
    disconnect_all()

    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(1,int(num)+1):
        for j in xrange(0,3):
            t = Multi_ExecThread(i, 8983+j, queue)
            threads.append(t)

    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    #results = execute(sudo_java_run)
    timeregex = re.compile('.*\s.*\s.*\s.*\s.*\sTime spent: 0:00:(.*)')
    timestamps = []
    for message in messages:
        for result in message.itervalues():
            match = timeregex.match(result).group(1)
            timestamps.append(float(match))

    print timestamps
    print "avg : %f" % (sum(timestamps,0.0)/len(timestamps))

class ExecThread(threading.Thread):
    def __init__(self, i, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.queue = queue

    def run(self):
        results = execute(java_run, i=self.i)
        self.queue.put(results)

class Multi_ExecThread(threading.Thread):
    def __init__(self, i, port, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.port = str(port)
        self.queue = queue

    def run(self):
        results = execute(multi_java_run, port=self.port, i=self.i)
        self.queue.put(results)

def resource_monitor():
    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(1,int(num)+1):
        t = ExecThread(i, queue)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    #results = execute(sudo_java_run)
    timeregex = re.compile('.*\s.*\s.*\s\+\+\+(.*)\-\-\-')
    timestamps = []
    for message in messages:
        for result in message.itervalues():
            match = timeregex.match(result).group(1)
            timestamps.append(float(match))

    print timestamps
    print "avg : %f" % (sum(timestamps,0.0)/len(timestamps))

class MonitorThread(threading.Thread):
    def __init__(self, i, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.queue = queue

    def run(self):
        results = execute(java_run, i=self.i)
        self.queue.put(results)
