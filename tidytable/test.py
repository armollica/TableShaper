import os
import sys

commands_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands/cli'))

def list_commands():
    commands = []
    for filename in os.listdir(commands_folder):
        if filename.endswith('_cli.py'):
            commands.append(filename[0:-7])
    commands.sort()
    return commands

def get_command(name):
    try:
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        module_name = 'tidytable.commands.cli.' + name + '_cli'
        import_list = ['cli']
        module = __import__(module_name, None, None, import_list)
    except ImportError:
        return
    return module.cli

print get_command('mutate')