#!/bin/bash
sleep 10
echo ${ZOOKEEPER_MYID} > /var/lib/zookeeper/myid
/opt/zookeeper/bin/zkServer.sh start

hostname=$(hostname)
echo > /tmp/output.log

echo "$(date): zookeepr init" >> /tmp/output.log
/opt/message/zookeeper_init.py ${hostname} 3 60
RET=$?
echo "$(date): zookeepr done ${RET}" >> /tmp/output.log

/opt/message/zookeeper_message.py recv node02done 60 >> /tmp/output.log
echo "$(date): Jenkins Server start" >> /tmp/output.log
sleep 3
echo "$(date): Jenkins Server done" >> /tmp/output.log
