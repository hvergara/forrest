import sys
from forrest.commands import run

COMMANDS = ['run']

def cli():

  if len(sys.argv) == 1 or sys.argv[1] not in COMMANDS:
    print('Usage:')
    print('  forrest run [app-name]')
    sys.exit(1)

  command = sys.argv[1]

  if command == 'run':
    run.process(sys.argv[2:])

