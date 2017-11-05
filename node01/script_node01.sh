#!/bin/bash
echo ${ZOOKEEPER_MYID} > /var/lib/zookeeper/myid
/opt/zookeeper/bin/zkServer.sh start

hostname=$(hostname)
echo > /tmp/output.log

echo "$(date): zookeepr init" >> /tmp/output.log
/opt/message/zookeeper_init.py ${hostname} 3 60
RET=$?
echo "$(date): zookeepr done ${RET}" >> /tmp/output.log

echo "$(date): DB Server setup start" >> /tmp/output.log
sleep 8
echo "$(date): DB Server DB initialized" >> /tmp/output.log
/opt/message/zookeeper_message.py send node01done "${hostname} done" 60
RET=$?
sleep 5
echo "$(date): DB Server setup done ${RET}" >> /tmp/output.log
