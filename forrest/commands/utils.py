import os
import re
import subprocess
import shlex
from ConfigParser import SafeConfigParser

CONFIG_FILE = os.path.join(os.getcwd(), '.forrest')


def get_config():
  config = SafeConfigParser()
  config.read(CONFIG_FILE)

  return config


def save_config(config):
  config.write(open(CONFIG_FILE, 'w'))


def get_input(text, default=''):
  response = raw_input(text)

  if len(response) == 0:
    response = default

  return response


def create_bundle(source_dir):
  local_command('tar czf /tmp/bundle.tgz -C %s .' % source_dir)


def local_command(command, decoder=None, tty=None):

  if tty:
    return os.system(command)
  
  else:
    dev_null = open(os.devnull, 'w')
    output = subprocess.check_output(shlex.split(command))
    dev_null.close()

    if decoder:
      return decoder(output)
    else:
      return output
