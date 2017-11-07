import json
import sys
import os
import subprocess
import time
from forrest.providers import BaseInstance


class Instance(BaseInstance):

  def __init__(self, config):
    self.config = config


  def cli(self, command, arguments, decoder=None):
    return self.local_command('aws ec2 %s %s' % (command, arguments), decoder=decoder)


  def start(self):
    security_group_id = self.create_security_group()

    if not security_group_id:
      print('[!] Error creating security group')
      sys.exit(1)

    cli_args = self.config['options']
    cli_args +=  ' --security-group-ids %s' % security_group_id

    self.authorize_security_group_ssh(security_group_id)

    self.instance_id = self.create_instance(cli_args)

    self.public_ip = self.get_public_ip()


  def create_instance(self, cli_args):
    self.log('Creating instance... ', nl=False)

    response = self.cli('run-instances', cli_args, decoder=json.loads)

    instance_id = None
  
    try:
      instance_id = response['Instances'][0]['InstanceId']
      self.log(instance_id)
    except:
      self.log('ERROR')
      pass
  
    return instance_id
  

  def create_security_group(self):
    self.log('Creating Security Group... ', nl=False)

    group_name = 'forrest-%s' % int(time.time() * 100000)
    group_id = None
  
    try:
      cli_args = '--group-name %s --description %s' % (group_name, group_name)
      response = self.cli('create-security-group', cli_args, decoder=json.loads)

      group_id = response['GroupId']
      self.log(group_id)

    except Exception, e:
      self.log('ERROR: ' + str(e))
      pass

    return group_id


  def remove_security_group(self, group_id):
    self.log('Removing Security Group...', nl=False)

    for i in range(0, 60):
      try:
        self.cli('delete-security-group', '--group-id %s' % group_id)
        self.log(' OK')
        return True

      except:
        self.log('.', nl=False)

    self.log(' ERROR')


  def authorize_security_group_ssh(self, group_id):
    self.log('Authorizing SSH for security group [%s]... ' % group_id, nl=False)
    cli_args = '--group-id %s --protocol tcp --port 22 --cidr 0.0.0.0/0' % group_id
    self.cli('authorize-security-group-ingress', cli_args)
    self.log(' OK')


  def get_public_ip(self, timeout=60):
    self.log('Waiting for Public IP...', nl=False)

    for attempt in range(0, timeout):
      try:
        cli_args = '--instance-ids %s' % self.instance_id
        response = self.cli('describe-instances', cli_args, decoder=json.loads)
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        break

      except Exception, e:
        self.log('.', nl=False)
        time.sleep(1)

    else:
      public_ip = None

    self.log(' ' + public_ip)

    return public_ip


  def terminate(self, timeout=60):
    self.log('Finishing instance... ', nl=False)
    self.cli('terminate-instances', '--instance-ids %s' % self.instance_id)
    self.log('OK')
