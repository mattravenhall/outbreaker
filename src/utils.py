#!/usr/bin/env python3

import sys

def binary_query(query, default=False):
    if default:
        reply = input(f"{query} (Y/n): ")
    elif not default:
        reply = input(f"{query} (y/N): ")
    else:
        raise ValueError('Inappropriate default value passed to binary_query.')

    if reply.lower() in ['yes', 'y', 'true', 't']:
        return True
    elif reply.lower() in ['no', 'n', 'false', 'f']:
        return False
    else:
        return default

def int_query(query, minVal=None, maxVal=None):
    if minVal is None: # no floor
        if isinstance(maxVal, int): # a ceiling
            reply = input(f"{query} (max {maxVal}): ")
        else: # Max isn't an int, so default to no maxlimit
            reply = input(f"{query}")
    elif maxVal is None: # no ceiling
        if instance(minVal, int): # a floor
            reply = input(f"{query} (min {minVal}): ")
        else: # Min isn't an int, so default to no minlimit
            reply = input(f"{query}")
    else: # limits
        reply = input(f"{query} ({minVal}-{maxVal}): ")

    # Check an int was provided
    try:
        reply = int(reply)
        if reply < minVal:
            self.error("Provided integer too small.")
            sys.exit(-1)
        elif reply > maxVal:
            self.error("Provided integer too large.")
            sys.exit(-1)
        else:
            return(reply)       
    except ValueError:
        if reply.lower() not in ['n','no','false','f','']:
            self.error(f"Expect an integer but received '{query}'")
        sys.exit(-1)
