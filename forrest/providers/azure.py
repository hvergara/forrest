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
    return self.local_command('az vm %s %s' % (command, arguments), decoder=decoder)


  def start(self):
    cli_args = self.config['options']

    self.create_instance(cli_args)
    self.public_ip = self.get_public_ip()


  def create_instance(self, cli_args):
    self.log('Creating instance... ', nl=False)

    instance_id = cli_args.get('-n', 'forrest-%s' % int(time.time() * 100000))
    cli_args['-n'] = instance_id

    self.log(' ' + instance_id)

    response = self.cli('create', cli_args, decoder=json.loads)

    try:
      self.public_ip = response['publicIpAddress']
    except:
      self.log('ERROR')
      pass
  
    return instance_id
  

  def get_public_ip(self, timeout=60):
    self.log('Waiting for Public IP... ', nl=False)

    if self.public_ip:
      self.log(self.public_ip)
      return self.public_ip

    return None


  def terminate(self, timeout=60):
    self.log('Finishing instance... ', nl=False)
    self.cli('delete', '--resource-group %s --name %s --yes' % (self.resource_group, self.instance_name))
    self.log('OK')

