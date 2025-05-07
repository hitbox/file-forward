import os
import socket
import subprocess

import click

from zxcvbn import zxcvbn

instance_dirs = [
    'instance/archive',
    'instance/certs',
    'instance/config',
    'instance/etc',
    'instance/logging',
]

default_client_cert_path = 'instance/certs/client.kdb'
default_server_cert_path = 'instance/certs/mqssl_stage.crt'

class StrictPath(click.Path):
    """
    click.Path with extra path checks.
    """

    def __init__(self, *args, **kwargs):
        self.extension = kwargs.pop('extension', None)
        super().__init__(*args, **kwargs)

    def convert(self, value, param, ctx):
        path = super().convert(value, param, ctx)

        if self.extension:
            ext = self.extension.lower()
            if not path.lower().endswith(ext):
                self.fail(f'Path must end with {ext}.', param, ctx)

        return path

def check_sanity():
    """
    Check system dependencies.
    """
    try:
        subprocess.run(['runmqakm', '-version'], check=True, capture_output=True)
    except FileNotFoundError:
        click.error('Error: IBM MQ command "runmqakm" not found.', err=True)
        raise click.Abort()

def get_hostname():
    return socket.gethostname()

def get_default_label():
    return get_hostname() + '-crew-brief'

def get_commands(
    database_path,
    password,
    cert_label,
    server_cert_path,
    distinguished_name,
    expire_days = 3650,
):
    commands = [
        {
            'message': 'Create client key database',
            'command': [
                'runmqakm', '-keydb', '-create',
                '-db', database_path,
                '-pw', password,
                '-stash',
                '-expire', f'{expire_days}',
            ],
        },
        {
            'message': 'Create and add client certificate to database',
            'command': [
                'runmqakm', '-cert', '-create',
                '-db', database_path,
                '-label', cert_label,
                '-stashed',
                '-size', '2048', # Key size in bits.
                '-sigalg', 'SHA512WithRSA',
                '-expire', f'{expire_days}',
                '-dn', distinguished_name,
            ],
        },
        {
            'message': 'Add server trust certificate',
            'command': [
                'runmqakm', '-cert', '-add',
                '-file', server_cert_path,
                '-trust', 'enable',
                '-db', database_path,
                '-stashed',
            ],
        },
    ]
    return commands

def input_kdb_path():
    """
    Prompt until non-existing .kdb path is given.
    """
    while True:
        kdb_path = click.prompt(
            'Path to client .kdb file',
            default = default_client_cert_path,
            type = StrictPath(
                extension = '.kdb',
            ),
        )
        if not os.path.exists(kdb_path):
            break
        click.echo('Client database already exists.')
    return kdb_path

def input_distinguished_name():
    """
    Prompt and assemble distinguished name string.
    """
    distinguished_name = {}
    distinguished_name['CN'] = click.prompt('Common Name', default=get_hostname())
    distinguished_name['O'] = click.prompt('Organization', default='', show_default=False)
    distinguished_name['C'] = click.prompt('Country Code', default='', show_default=False)
    distinguished_name = ','.join(f'{key}={val}' for key, val in distinguished_name.items() if val)
    return distinguished_name

def input_strong_password():
    """
    Prompt until given a strong password.
    """
    while True:
        password = click.prompt(
            'Key database password',
            hide_input = True,
            confirmation_prompt = True,
        )
        pw_strength = zxcvbn(password)
        if pw_strength['score'] < 3:
            click.secho('Password is weak.', fg='red')
        else:
            break
    return password

def execute_commands(password, commands, echo):
    for command in commands:
        click.echo(command['message'])
        cmd = command['command']
        if echo:
            masked = cmd.copy()
            if password in masked:
                masked[masked.index(password)] = '*' * 8
            click.secho(subprocess.list2cmdline(masked), fg='cyan')
        cmd_result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if echo:
            if cmd_result.stdout:
                click.secho(cmd_result.stdout.strip(), fg='green')
            if cmd_result.stderr:
                click.secho(cmd_result.stderr.strip(), fg='red')

@click.command()
@click.option('--echo/--no-echo', help='Echo commands.')
def main(echo):
    """
    Interactive command line tool to assist setting up a new instance,
    especially for creating the key database file.
    """
    check_sanity()

    # Gather input from user.
    kdb_path = input_kdb_path()
    server_cert_path = click.prompt(
        'Path to server trust cert',
        default = default_server_cert_path,
        type = click.Path(
            exists = True, # Must exist.
        ),
    )
    cert_label = click.prompt('Certificate label', default=get_default_label())
    distinguished_name = input_distinguished_name()
    password = input_strong_password()

    # Construct commands.
    commands = get_commands(kdb_path, password, cert_label, server_cert_path, distinguished_name)

    # Ensure instance directory structures.
    for dirpath in instance_dirs:
        os.makedirs(dirpath, exist_ok=True)

    # Execute commands
    execute_commands(password, commands, echo)

if __name__ == '__main__':
    main()
