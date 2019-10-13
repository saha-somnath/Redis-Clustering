#!/usr/bin/python

import os,sys
import argparse
import textwrap
from redis_cluster import RedisCluster


def commandLineArguments():
    """
    Process command line arguments
    :return: <dict> A dictionary of parameters
    """
    desc = textwrap.dedent('''
    Publish a message to a channel/queue.
    cmd:
    $python Redis_Cluster_Publish.py -c <channel> -m <message>
    ''')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=desc)
    parser.add_argument('--channel', '-c', default="CH", help="Channel Name")
    parser.add_argument('--message', '-m', help="Message in JSON format")

    args = vars(parser.parse_args())
    print(args)
    return args

def main():

    args = commandLineArguments()
    channel = args["channel"]
    message = args["message"]

    # Invoke queue and message
    rc = RedisCluster()
    print(rc.ping())
    rc.publish(channel, message)
	



if __name__ == "__main__":
    main()
