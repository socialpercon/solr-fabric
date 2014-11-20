#!/usr/bin/python
# coding: utf-8
import yaml
import sys
import argparse
import os
from fabric.api import env
from fabrication.util.fabrickit import *

f = open("./config/solr_fabric.yml", 'r')
config = yaml.safe_load(f)


#filedaemon execute
   #how to confirm the time
filedaemon_parser = argparse.ArgumentParser()

@run_multiple
def filedaemon(*agrs, **kwargs):
    run('python %s/multi_file_daemon.py %s/%s' % config['path.data'], config['path.data'], config['path.data.dir'])

def multi_filedaemon():
    filedaemon(hosts=config['dataset.hosts'])

@run_multiple
def put_filedaemon(*agrs, **kwargs):
    put('./scripts/multi_file_daemon.py', config['path.data'], use_sudo=False)

def multi_put_filedaemon():
    put_filedaemon(hosts=config['dataset.hosts'])

#post.jar copy and execute for count on filedaemon
post_parser = argparse.ArgumentParser()
@run_multiple
def post(*agrs, **kwargs):
    run('%s/start-post.sh' % config['path.data'])

def multi_post():
    post(hosts=config['dataset.hosts'])

@run_multiple
def put_post_script():
    put('./scripts/post.sh', config['path.data'], use_sudo=False)

def multi_put_script(*args, **kwargs):
    put_post_script(hosts=config['dataset.hosts'])

#dataset???
send_parser = argparse.ArgumentParser()
def send(args, help=False):
    #put()


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
