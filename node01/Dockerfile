FROM centos

RUN yum update -y
RUN yum install -y \
  curl \
  java \
  unzip

WORKDIR /opt
RUN curl -O http://ftp.jaist.ac.jp/pub/apache/zookeeper/current/zookeeper-3.4.10.tar.gz
RUN tar xvf zookeeper-3.4.10.tar.gz
RUN rm -f zookeeper-3.4.10.tar.gz
RUN ln -s zookeeper-3.4.10 zookeeper
RUN cp /opt/zookeeper/conf/zoo_sample.cfg /opt/zookeeper/conf/zoo.cfg
RUN sed -i '/^dataDir=/s:=.*:=/var/lib/zookeeper:' /opt/zookeeper/conf/zoo.cfg
COPY server.txt /tmp
RUN cat /tmp/server.txt >> /opt/zookeeper/conf/zoo.cfg
RUN mkdir /var/lib/zookeeper

RUN yum install -y epel-release
RUN yum install -y python-pip supervisor
RUN pip install kazoo

RUN mv /etc/supervisord.conf{,.bak}
COPY supervisord.conf /etc

RUN mkdir /opt/init
COPY init.sh /opt/init

RUN mkdir /opt/message
COPY zookeeper_start.sh /opt/message
COPY script_node01.sh /opt/message
COPY script_node02.sh /opt/message
COPY script_node03.sh /opt/message
COPY zookeeper_init.py /opt/message
COPY zookeeper_message.py /opt/message

CMD /usr/bin/supervisord
