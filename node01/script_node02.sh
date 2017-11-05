#!/bin/bash
echo ${ZOOKEEPER_MYID} > /var/lib/zookeeper/myid
/opt/zookeeper/bin/zkServer.sh start

hostname=$(hostname)
echo > /tmp/output.log

echo "$(date): zookeepr init" >> /tmp/output.log
/opt/message/zookeeper_init.py ${hostname} 3 60
RET=$?
echo "$(date): zookeepr done ${RET}" >> /tmp/output.log

echo "$(date): AP Server setup wait" >> /tmp/output.log
sleep 5
/opt/message/zookeeper_message.py recv node01done 60 >> /tmp/output.log
echo "$(date): AP Server setup start" >> /tmp/output.log
RET=$?
sleep 10
echo "$(date): AP Server setup end ${RET}" >> /tmp/output.log
/opt/message/zookeeper_message.py send node02done "${hostname} done" 60
RET=$?
echo "$(date): AP Server setup done ${RET}" >> /tmp/output.log
