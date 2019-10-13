# Redis-Clustering
Redis is an in-memory distributed key-value database. It also can be used as Message Queue with (PUB/SUB) patterns. With the cluster setup, redis provide high availability, persistence, simple and faster access of data. Here is the instruction of creating redis cluster from scratch.   
Redis Version: 5.0.3
## Installation: https://redis.io/download
```
$ wget http://download.redis.io/releases/redis-5.0.3.tar.gz
$ tar xzf redis-5.0.3.tar.gz
$ cd redis-5.0.3
$ make
```
## General Configuration: Redis use “/etc/redis.conf” file as default configuration file. 
```
- Start redis instance with default configuration file.
$redis-server &
- Start redis with a configuration file.
$redis-server /home/Redis/redis_cluster/7000/redis.conf &
- It also can be launched as systemctl process.
$
```
### Redis Cluster Setup:
By default redis requires six instance to start a cluster. Create six redis instance in six different (preferred) or same machine. I have cluster running in four following servers.
 ```
 server1: 10.x.x.1   
 server2: 10.x.x.2
 server3: 10.x.x.3  
 server4: 10.x.x.4 
	
root      xxxx1      1  0 Dec1 ?        00:01:08 redis-server 10.x.x.1:7000 [cluster]
root      xxxx2      1  0 Dec1 ?        00:02:41 redis-server 10.x.x.4:7003 [cluster]
root      xxxx3      1  0 Dec1 ?        00:03:43 redis-server 10.x.x.4:7005 [cluster]
root      xxxx4      1  0 Dec1 ?        00:04:39 redis-server 10.x.x.2:7001 [cluster]
root      xxxx5      1  0 Dec1 ?        00:05:58 redis-server 10.x.x.3:7004 [cluster]
root      xxxx6      1  0 Dec1 ?        00:06:23 redis-server 10.x.x.3:7002 [cluster]

- At a time three redis cluster instance work as master and three as slave.
 redis-server 10.x.x.4:7003 [cluster] - S1 -> M1
 redis-server 10.x.x.4:7005 [cluster] - S3 -> M3
 redis-server 10.x.x.3:7002 [cluster]   - M3 <- S3
 redis-server 10.x.x.3:7004 [cluster]   - S2 -> M2
 redis-server 10.x.x.2:7001 [cluster]  - M2 <- S2
 redis-server 10.x.x.1:7000 [cluster]   - M1 <- S1
 ```

- Persistent mode is set. ( appendonly  yes )
- Redis Availability:  The redis cluster is designed the survive failure with few nodes. In case of failure of master, the cluster re-configure the system and promote the corresponding slave to become master. 
o Automatic detection of non-working cluster node (master) and promote slave to master.
o All the nodes are connected using TCP bus and a binary protocol called a Redis Cluster Bus.
o Nodes use a gossip protocol to propagate information about the cluster in order to discover new nodes, to send ping packets to make sure all the other nodes are working properly, and to send cluster messages needed to signal specific conditions
o Cluster bus is used to propagate PUB/SUB messages.
o Improved availability with replication migration feature. In case of master no longer replicated by a slave will receive a slave from master have multiple slaves.
### Create Redis Cluster:
```
o Command:
$redis-cli --cluster create 10.x.x.1:7000 10.x.x.2:7001 
              10.x.x.3:7002 10.x.x.3:7004  10.x.x.4:7003 10.x.x.4:7005  --cluster-replicas 1
o “—cluster-replicas”: Specify number of replica/slave for each master.

- Check cluster:
$redis-cli --cluster check 10.x.x.4:7003

10.x.x.1:7000 (4867b620...) -> 0 keys | 5461 slots | 1 slaves.
10.x.x.2:7001 (efbadeac...) -> 0 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
### Testing Cluster: 
- Example of covering a master
o Manual shutdown of 10.x.x.2:7001  redis master node. Slave 10.x.x.3:7004 becomes master.
```
redis-cli --cluster check 10.x.x.4:7003
Could not connect to Redis at 10.x.x.2:7001: Connection refused
10.x.x.1:7000 (4867b620...) -> 0 keys | 5461 slots | 1 slaves.
10.x.x.3:7004 (de14cae1...) -> 0 keys | 5462 slots | 0 slaves.
10.x.x.3:7002 (a17fe73f...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots:[5461-10922] (5462 slots) master
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
- Bring back the shutdown node (10.x.x.2:7001) alive which become slave of new master (10.x.x.3:7004)
```
o	redis-cli --cluster check 10.x.x.4:7003
10.x.x.1:7000 (4867b620...) -> 0 keys | 5461 slots | 1 slaves.
10.x.x.3:7004 (de14cae1...) -> 0 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots: (0 slots) slave
   replicates de14cae1e75a4da2bcee1e9e66f666f8111cffe4
M: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
### Example of PUB/SUB in python
o Subscribe to a channel, say CH, using python script Redis_Cluster_Subscribe.py.
```
[root@server1 Redis]# python Redis_Cluster_Subscribe.py
INFO: Connection established with node [{'host': '10.x.x.1', 'port': 7000}, {'host': '10.x.x.3', 'port': 7002}]
INFO: Subscribing to the channel CH
1
{u'node': u'NODE-1', u'timestamp': u'110000223334', u'args': {u'node': u'NODE-1', u'cluster': u'CLUSTER-1'}, u'name': u'CM_NODE_UP'}
o	Publish a message to that channel using Redis_Cluster_Publish.py script.
root@server4:/home/Redis# python Redis_Cluster_Publish.py CH '{"name": "CM_NODE_UP","node": "NODE-1","args": {"node": "NODE-1", "cluster": "CLUSTER-1"},"timestamp": "110000223334"}'
INFO: Connection established with node [{'host': '10.x.x.1', 'port': 7000}, {'host': '10.x.x.3', 'port': 7002}]
INFO: Channel-CH , Message-"{"name": "CM_NODE_UP","node": "NODE-1","args": {"node": "NODE-1", "cluster": "CLUSTER-1"},"timestamp": "110000223334"}"
root@server4:/home/Redis#
```
- Example of PUB/SUB using Python and C++ api.
o Subscribe to a channel, say CH, using C++ api.
```
root@server3:/home/Redis# ./cpp_redis_subscriber CH
INFO: Subscribing to a channel CH
MESSAGE CH: {"name": "CM_NODE_UP","node": "NODE-1","args": {"node": "NODE-1", "cluster": "CLUSTER-1"},"timestamp": "110000223334"}
o	Publish a message to the channel.
[root@server1 Redis]# python Redis_Cluster_Publish.py CH '{"name": "CM_NODE_UP","node": "NODE-1","args": {"node": "NODE-1", "cluster": "CLUSTER-1"},"timestamp": "110000223334"}'
INFO: Connection established with node [{'host': '10.x.x.1', 'port': 7000}, {'host': '10.x.x.3', 'port': 7002}]
INFO: Channel-CH , Message-"{"name": "CM_NODE_UP","node": "NODE-1","args": {"node": "NODE-1", "cluster": "CLUSTER-1"},"timestamp": "110000223334"}"
[root@server1 Redis]#
```


### The redis client for Python and C++:
- Python Client:
o Installation:
 $pip install redis
 $pip install redis-py-cluster
o Sample Code to publish and subscribe to a channel.
/home/Redis/Redis_Cluster.py
/home/Redis/Redis_Cluster_Publish.py
/home/Redis/Redis_Cluster_Subscribe.py
#### Execution:
 $python Redis_Cluster_Subscribe.py <Channel>
 $python Redis_Cluster_Publish.py <Channel> <Message>

- C++ Client:
o Installation: https://github.com/Cylix/cpp_redis/wiki/Mac-&-Linux-Install
 Steps:
```
- Clone the project
$git clone https://github.com/Cylix/cpp_redis.git
- Go inside the project directory
$cd cpp_redis
- Get tacopie submodule
git submodule init && git submodule update
- Create a build directory and move into it
$mkdir build && cd build
- Generate the Makefile using CMake
$cmake .. -DCMAKE_BUILD_TYPE=Release
# Build the library
$make
# Install the library
$make install
```
o Sample Code to subscribe to a channel:
```
 Source code & Example:
/home/Redis/cpp_redis
/home/Redis/cpp_redis_subscriber.cpp
 Compile:
$ g++ cpp_redis_subscriber.cpp -o cpp_redis_subscriber -pthread -std=gnu++11 -lcpp_redis –ltacopie
 Execution:
$/home/Redis/cpp_redis_subscriber  <Channel>
```


### How to add a new node:
- Launch a new redis instance and join that to the existing cluster.
- Cluster with 6 nodes:
```
root@server3:/home/Redis# redis-cli --cluster check 10.x.x.4:7003
10.x.x.1:7000 (4867b620...) -> 1 keys | 5461 slots | 1 slaves.
10.x.x.2:7001 (efbadeac...) -> 1 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 2 keys | 5461 slots | 1 slaves.
[OK] 4 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
- Add new node 10.x.x.5:7010
```
root@server3:/home/Redis# redis-cli --cluster add-node 10.x.x.5:7010 10.x.x.3:7002
>>> Adding node 10.x.x.5:7010 to cluster 10.x.x.3:7002
>>> Performing Cluster Check (using node 10.x.x.3:7002)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
>>> Send CLUSTER MEET to node 10.x.x.5:7010 to make it join the cluster.
[OK] New node added correctly.

root@server3:/home/Redis# redis-cli --cluster check 10.x.x.4:7003
10.x.x.1:7000 (4867b620...) -> 1 keys | 5461 slots | 1 slaves.
10.x.x.5:7010 (f8c32134...) -> 0 keys | 0 slots | 0 slaves.
10.x.x.2:7001 (efbadeac...) -> 1 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 2 keys | 5461 slots | 1 slaves.
[OK] 4 keys in 4 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: f8c32134b98c04e6dbf5c4067044ec43483cdf62 10.x.x.5:7010
   slots: (0 slots) master
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

```

### Testing:
• Abrupt reboots skipping all unmounts-
```
$ echo o>/proc/sysrq-trigger
root@msl-ssg-dl14 Redis]echo b > /proc/sysrq-trigger
packet_write_wait: Connection to 10.x.x.5 port 22: Broken pipe
-bash-4.2$
[root@server1 Redis]# redis-cli --cluster check 10.x.x.4:7003
Could not connect to Redis at 10.x.x.5:7010: Connection refused
10.x.x.1:7000 (4867b620...) -> 1 keys | 5461 slots | 1 slaves.
10.x.x.2:7001 (efbadeac...) -> 1 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 2 keys | 5461 slots | 1 slaves.
[OK] 4 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

[root@server1 Redis]# redis-cli --cluster check 10.x.x.4:7003
10.x.x.1:7000 (4867b620...) -> 1 keys | 5461 slots | 1 slaves.
10.x.x.5:7010 (f8c32134...) -> 0 keys | 0 slots | 0 slaves.
10.x.x.2:7001 (efbadeac...) -> 1 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 2 keys | 5461 slots | 1 slaves.
[OK] 4 keys in 4 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: f8c32134b98c04e6dbf5c4067044ec43483cdf62 10.x.x.5:7010
   slots: (0 slots) master
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

• Turn off the machine with “echo o > /proc/sysrq-trigger”
```
root@msl-ssg-dl14 7010]echo o > /proc/sysrq-trigger
root@msl-ssg-dl14 7010]packet_write_wait: Connection to 10.x.x.5 port 22: Broken pipe

[root@server1 Redis]# redis-cli --cluster check 10.x.x.4:7003
Could not connect to Redis at 10.x.x.5:7010: No route to host
10.x.x.1:7000 (4867b620...) -> 1 keys | 5461 slots | 1 slaves.
10.x.x.2:7001 (efbadeac...) -> 1 keys | 5462 slots | 1 slaves.
10.x.x.3:7002 (a17fe73f...) -> 2 keys | 5461 slots | 1 slaves.
[OK] 4 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 10.x.x.4:7003)
S: 36cd1725c923475acd3a70b1080c0ab27bab15e0 10.x.x.4:7003
   slots: (0 slots) slave
   replicates 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0
S: de14cae1e75a4da2bcee1e9e66f666f8111cffe4 10.x.x.3:7004
   slots: (0 slots) slave
   replicates efbadeacde045b9d675ae8c92336b3eb07b1bf1f
S: 12f763693beffb36c1122f8cd7b5ea0ebed8612a 10.x.x.4:7005
   slots: (0 slots) slave
   replicates a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd
M: 4867b6208364a7a93b1c524b7ffc7cc0b1d184f0 10.x.x.1:7000
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: efbadeacde045b9d675ae8c92336b3eb07b1bf1f 10.x.x.2:7001
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: a17fe73f8f0ca6fd044ef5ecc79ea7e12b9d25cd 10.x.x.3:7002
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
