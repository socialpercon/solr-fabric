#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import re

env.parallel = True
my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175','logstash@192.168.0.176']
#my_hosts = ['logstash@192.168.0.170']
env.password = 'hello.logstash'

#Command
command = "java -jar thriftclient-0.0.1-SNAPSHOT-jar-with-dependencies.jar"
file_directory = "/home/logstash/solr-4.7.2/example/exampledocs"

#Java
jar_name = 'thriftclient-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
jar_path = "./target/" + jar_name

#Docs
docs_path = './json_data/'

@hosts(my_hosts)
def java_run():
    global command
    global file_directory
    
	# file
    for i in xrange(0,1):
        put("%s%s-%d.json" % (docs_path,env.host, i), file_directory, use_sudo=False);


  
def sudo_java_run(command):
    sudo(command)

def merge_results_with_file():
    execute(file_put)
    merge_results()

def merge_results():
    results = execute(java_run)
    #results = execute(sudo_java_run)
