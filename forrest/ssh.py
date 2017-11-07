from forrest.commands.utils import local_command

class UnixSSHClient:

  def __init__(self, hostname, username, password=None, private_key=None):
    self.hostname = hostname
    self.username = username
    self.password = password
    self.private_key = private_key


  def copy(self, source, destination):
    args = [
      'scp',
      '-o', 'StrictHostKeyChecking=no',
      '-o', 'LogLevel=quiet',
      '-i', self.private_key,
      source,
      '%s@%s:~/%s' % (self.username, self.hostname, destination)
    ]

    local_command(' '.join(args))


  def exec_command(self, command, tty=None):

    args = [
      'ssh',
      '-o', 'StrictHostKeyChecking=no',
      '-o', 'LogLevel=quiet',
      '-i', self.private_key
    ]
    
    if tty:
      args.append('-t')
      
    args.extend([
      '%s@%s' % (self.username, self.hostname),
      '"%s"' % command
    ])

    local_command(' '.join(args), tty=tty)