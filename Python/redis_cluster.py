#!/usr/bin/python
import os,sys
import json
from rediscluster import StrictRedisCluster


class RedisCluster:
    """
    Class: Redis Cluster
    Connect to the redis cluster.
    """
    CONFIG = "cluster_config.json"

    def __init__(self):
        self.config        = self.getClusterConfig()
        self.startup_nodes = self.getClusterMachine()
        self.connection = self.connect()


    def getClusterMachine(self):
        cluster_machine = self.config.get('machine', [{"host": '10.1.51.2', "port": 7000}, {"host": '10.1.51.3', "port": 7002}])
        #print("INFO: Cluster machines ...\n {}".format(cluster_machine))
        return cluster_machine

    def getClusterConfig(self):
        with open(RedisCluster.CONFIG, "r") as CFG:
            config = json.load(CFG)

        return config

    def connect(self):
        """
        Connect to cluster
        :return: connection object
        """
        print("INFO: Connection established with cluster {} ".format(self.startup_nodes))
        con = StrictRedisCluster(startup_nodes=self.startup_nodes, decode_responses=True)
        return con

    def publish(self, channel="CH", message="Test Message"):
        """
        Publish the message to the specified channel
        :param channel: <string> - Channel name
        :param message: <string> - Message to be sent to subscribers
        :return: None
        """
        con = self.connection
        print("INFO: Channel: {} , Message: \"{}\"".format(channel, message))
        con.publish(channel, message)

    def subscribe(self,channel="CH"):
        """
        Subscribe to a channel to receive published message
        :param channel: <string> - channel name
        :return: subscribe
        """
        print("INFO: Subscribing to the channel {}".format(channel))
        con = self.connection
        queue =  con.pubsub()
        queue.subscribe(channel)

        return queue


    def ping(self):
        con = self.connection
        print(con.ping())
        return "PONG"
