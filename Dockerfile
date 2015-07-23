FROM centos:centos7

RUN yum -y update && yum clean all
RUN yum install -y git python-devel python-virtualenv \
    epel-release libxml2-devel libxslt-devel 
