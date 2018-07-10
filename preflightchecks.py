#!/usr/bin/env python3
import os
import sys
import stat
import platform
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
        raise ValueError('Inappropriate default value passed to binary_query.')

    if reply.lower() in ['yes', 'y', 'true', 't']:
        return True
    elif reply.lower() in ['no', 'n', 'false', 'f']:
        return False
    else:
        return default

# Check required packages exist
print('Checking required packages are installed.')
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in installed_packages.split()]

with open("requirements.txt") as f:
    for package in f.readlines():
        package = package.rstrip('\n')

        install_check = importlib.find_loader(package)
        installed = install_check is not None

        if not installed: #package not in installed_packages:
            print("'{}' not found, please install before reattempting setup.".format(package))
            sys.exit()

# Set up PATH
if binary_query('Add outbreaker to PATH?'):
    if platform.system() == 'Darwin':
        add2path = subprocess.Popen("cp ~/.bash_profile ~/.bash_profile.save.preoutbreaker; echo '\n# Appended by outbreaker\n'export PATH='\"$PATH:{0}\"' >> ~/.bash_profile; chmod +x {0}/outbreaker".format(os.getcwd()), shell=True, stdout=subprocess.PIPE)
        add2path.wait()
        os.system('source ~/.bash_profile')
    else:
        add2path = subprocess.Popen("cp ~/.bashrc ~/.bashrc.save.preoutbreaker; echo '\n# Appended by outbreaker\n'export PATH='\"$PATH:{0}\"' >> ~/.bashrc; chmod +x {0}/outbreaker".format(os.getcwd()), shell=True, stdout=subprocess.PIPE)
        add2path.wait()
        os.system('bash; source ~/.bashrc')

print('Set up complete.')
