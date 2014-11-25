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
    #"dtach -n `mktemp -u /tmp/{}.XXXX` {}".format(sockname, cmd)
    cmd = 'python %s/filedaemon/multi_file_daemon.py %s/%s' % (config['path.data'], config['path.data'], config['path.source'][env.host_string])
    temp = '%s/filedaemon/filedaemon.sock' % config['path.data']
    run("dtach -n {} {}".format(temp, cmd))
    #run('cd %s/filedaemon && nohup ./filedaemon.sh &' % (config['path.data']), pty=False)
    #run('nohup %s/filedaemon/filedaemon.sh %s/filedaemon/multi_file_daemon.py %s/%s &' % (config['path.data'], config['path.data'], config['path.data'], config['path.data.dir']), pty=False)

def multi_filedaemon():
    filedaemon(hosts=config['dataset.hosts'])

@run_multiple
def put_filedaemon(*agrs, **kwargs):
    put('%s/scripts/filedaemon' % dir, config['path.data'], use_sudo=False)

def multi_put_filedaemon():
    put_filedaemon(hosts=config['dataset.hosts'])


@run_multiple
def attach():
    temp = '%s/filedaemon/filedaemon.sock' % config['path.data']
    run("dtach -a {}".format(temp))


def attach_filedaemon(args, help=False):
    attach(host=args.host)


@run_multiple
def _kill_filedaemon():
    temp = '%s/filedaemon/filedaemon.sock' % config['path.data']
    run('rm %s' % temp)
    run('ps axf | grep "multi_file_daemon.py" | grep -v grep | awk \'{print "kill -9 " $1}\' | sh', pty=False)

def kill_filedaemon(help=False):
    _kill_filedaemon(hosts=config['dataset.hosts'])


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
def _kill_solr():
    # Solr
    temp = '%s/solr.sock' % config['solr.home']
    run('rm %s' % temp)
    run('ps axf | grep "start.jar" | grep -v grep | awk \'{print "kill -9 " $1}\' | sh')



@run_multiple
def _solr():
    with cd(config['solr.home']):
        cmd = 'java -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -Dsolr.solr.home=multicore -jar start.jar'
        temp = '%s/solr.sock' % config['solr.home']
        run("dtach -n {} {}".format(temp, cmd))

def solr_start():
    temp = config['solr.hosts']
    _solr(hosts=temp)

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
