#!/usr/bin/env python3
import os
import sys
import stat
import importlib
import subprocess

# Intro text
print('Setting up Outbreaker on your system.')

# Core functions
def binary_query(query, default=False):
    if default:
        reply = input(query+' (Y/n): ')
    elif not default:
        reply = input(query+' (y/N): ')
    else:
        raise ValueError('Inappropriate default value passed to binary_query')

    if reply.lower() in ['yes', 'y', 'true', 't']:
        return True
    elif reply.lower() in ['no', 'n', 'false', 'f']:
        return False
    else:
        return default

# Check required packages exist
print('Checking required packages are installed')
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in installed_packages.split()]

with open("requirements.txt") as f:
    for package in f.readlines():
        package = package.rstrip('\n')

        install_check = importlib.find_loader(package)
        installed = install_check is not None

        if not installed: #package not in installed_packages:
            # if binary_query('Install {}?'.format(package)):
            #     install = subprocess.Popen('/usr/bin/env pip install {}'.format(package), shell=True, stdout=subprocess.PIPE)
            #     install.wait()
            # else:
            print("'{}' not found, please install before reattempting setup.".format(package))
            sys.exit()

# Set up PATH
if binary_query('Add outbreaker to PATH?'):
    add2path = subprocess.Popen("cp ~/.bashrc ~/.bashrc.save.preoutbreaker; echo export PATH='\"$PATH:{0}\"' >> ~/.bashrc; chmod +x {0}/outbreaker".format(os.getcwd()), shell=True, stdout=subprocess.PIPE)
    add2path.wait()
    os.system('. ~/.bashrc')

print('Set up complete.')