#!/usr/bin/python
# coding: utf-8
import json
import yaml
import sys
import argparse
import os
from fabric.api import env
from fabrication.util.fabrickit import *

dir = os.path.dirname( os.path.abspath( __file__ ) )
f = open("%s/config/solr_fabric.yml" % dir, 'r')
config = yaml.safe_load(f)


#filedaemon execute
   #how to confirm the time
filedaemon_parser = argparse.ArgumentParser()

@run_multiple
def filedaemon():
    run('python %s/filedaemon/multi_file_daemon.py %s/%s' % (config['path.data'], config['path.data'], config['path.data.dir']))

def multi_filedaemon():
    filedaemon(hosts=config['dataset.hosts'])

@run_multiple
def put_filedaemon(*agrs, **kwargs):
    put('%s/scripts/filedaemon' % dir, config['path.data'], use_sudo=False)

def multi_put_filedaemon():
    put_filedaemon(hosts=config['dataset.hosts'])

#post.jar copy and execute for count on filedaemon
post_parser = argparse.ArgumentParser()
@run_multiple
def post():
    run('%s/start-post.sh' % config['path.data'])

def multi_post():
    post(hosts=config['dataset.hosts'])

@run_multiple
def put_post_script():
    put('%s/scripts/post.sh' % dir, config['path.data'], use_sudo=False)

def multi_put_post_script():
    put_post_script(hosts=config['dataset.hosts'])

#dataset???
send_parser = argparse.ArgumentParser()
@run_multiple
def send(args):
    put(args, config['path.data'], use_sudo=False)

def target_send():
    temp = config['path.source']
    for target in temp:
        send(target.items()[0][0], host=target.items()[0][1])

@run_multiple
def start_solr():
    str = '%s/solr_clear_restart.sh' % config['solr.home']
    run(str)

def multi_start_solr():
    temp = config['solr.hosts']
    start_solr(hosts=temp)

@run_multiple
def put_solr_script():
    put('%s/scripts/solr_clear_restart.sh' % dir, config['solr.home'], use_sudo=False)

def multi_put_solr_script():
    put_solr_script(hosts=config['solr.hosts'])

def print_help(*args):
    if len(args) == 0:
        print "usage:"

def run_cmd(args):
    getattr(args[0])

def main():
    env.password=config['dataset.hosts.password']
    if len(sys.argv) < 2:
        print_help()
    else:
        run_cmd(sys.argv[1:])

if __name__ == '__main__':
    main()
