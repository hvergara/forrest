import os
import sys
import time
import socket
import subprocess
from forrest.commands.utils import local_command

class BaseInstance:

  def log(self, message, nl=True):
    if nl:
      sys.stdout.write(message + '\n')
    else:
      sys.stdout.write(message)

    sys.stdout.flush()

  def local_command(self, command, decoder=None):
    return local_command(command, decoder)

  def wait_for_ssh_ready(self, timeout=60):
    self.log('Waiting for SSH connection', nl=False)

    for i in range(0, timeout):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)

      result = sock.connect_ex((self.public_ip, 22))

      if result == 0:
        self.log(' OK')
        break

      else:
        self.log('.', nl=False)
        time.sleep(1)



def factory(provider):

  if provider == 'ec2':
    from . import ec2
    return ec2.Instance

  elif provider == 'azure':
    from . import azure
    return azure.Instance
  
  return None