#!/usr/bin/python

import os,sys
import argparse
import textwrap
import json
import time
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

    args = vars(parser.parse_args())
    return args

def get_message(queue=None):
    """
    Get the message from a subscribed channel
    :param queue: <string>
    :return: <string>
    """

    if queue:
        while True:
            msg = queue.get_message()
            ## take action
            if msg:
                data = msg['data']
                if isinstance(data, str) or isinstance(data, unicode):
                    try:
                        data = json.loads(data)
                    except Exception as e:
                        print("EXCEPTION: {} from \"{}\"".format(str(e), data))
                print(data)
            time.sleep(1)

def main():

    args = commandLineArguments()
    chan = args['channel']
    # Invoke queue and message
    rc = RedisCluster()
    queue = rc.subscribe(chan)
    get_message(queue)
    


if __name__ == "__main__":
    main()
