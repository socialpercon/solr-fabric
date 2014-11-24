import os
import sys


def main():
    #cmd = "ps -ef | grep %s | awk '{print $2}'" % sys.argv[1]
    cmd = """ps -ef | grep "start.jar" | awk '{print $2}'"""

    for chunk in os.popen(cmd):
        kill = """kill -9 %s""" % chunk 
        os.system(kill)

if __name__ == "__main__":
    main()
