import os
import sys
from forrest import providers
from forrest.commands.utils import get_config, local_command, create_bundle
from forrest.ssh import UnixSSHClient


def process(args):
  source_dir = os.getcwd()

  app_name = 'default'
  config = get_config()
  
  if len(args) > 0:
    app_name = args[0]

  if not app_name in config.sections():
    print("[!] App '%s' not found. Check your .forrest file." % app_name)
    sys.exit(1)


  app_config = dict(config.items(app_name))
  
  provider = providers.factory(app_config['provider'])

  if provider is None:
    print("[!] Provider '%s' not found" % app_config['provider'])
    sys.exit(1)

  instance = provider(app_config)
  instance.start()
  
  try:
    instance.wait_for_ssh_ready()

    print('Creating bundle...')
    create_bundle(source_dir)

    # Create ssh client
    ssh = UnixSSHClient(instance.public_ip, app_config['username'], private_key=app_config['private_key'])

    print('Uploading bundle...')
    ssh.copy('/tmp/bundle.tgz', 'bundle.tgz')
    ssh.exec_command('tar xzf bundle.tgz')

    print('Running process on remote server...')
    ssh.exec_command(app_config['command'], tty=True)

  except KeyboardInterrupt, e:
    print('\nCaught Ctrl-C. Terminating...')

  finally:
    instance.terminate()

