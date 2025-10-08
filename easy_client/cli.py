import argparse
import os
from pathlib import Path

from easy_client.commands import commands as cmd

cwd = os.getcwd()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The command to run (e.g. create)')
    args = parser.parse_args()

    if args.command == 'create':
        cmd.create(root=Path(cwd))
