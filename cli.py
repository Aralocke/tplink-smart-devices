#!/usr/bin/env python3

import argparse
import sys
from commands import Interactive, Poll, Status
from tplink.discover import LoadDevices
from tplink.utils import IsValidIPv4


def Main(args):
    for address in args.devices or []:
        if not IsValidIPv4(address):
            print("Error: Invalid IPv4 address: {}".format(address))
            return False

    devices = LoadDevices(args.devices)
    if args.devices and len(devices) == 0:
        print('Error: unable to load any devices')
        return False

    if args.command == 'status':
        return Status(devices, args)
    if args.command == 'poll':
        return Poll(devices, args)

    return Interactive(devices, args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('cli')
    parser.add_argument('--device', '-d', action='append', dest='devices',
        help='List of known devices. If provided discovery is skipped.')
    
    commands = parser.add_subparsers(dest='command')
    status = commands.add_parser('status',
        help='Get devices current status')

    args = parser.parse_args()
    if not Main(args):
        sys.exit(1)
    