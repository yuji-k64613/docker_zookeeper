#!/bin/sh
echo ${ZOOKEEPER_MYID} > /var/lib/zookeeper/myid
/opt/zookeeper/bin/zkServer.sh start-foreground
