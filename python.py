import socket
import pickle
## For CPU intensive tasking, don't use dummy. Dummy is threading, which is only run on one core of your CPU (Processes can be split amongst all cores).
from multiprocessing.dummy import Pool as ThreadPool
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
    pool = ThreadPool(3000)
    ## Arg1 should be a list in order for map to do its magic. 
    ## If not, use zip & itertools to send the same thing over and over to the function as needed.
    results = pool.map(start, arg1)

    pool.close()
    pool.join()
    
def start(arg1):
    ## do something

if __name__ == '__main__':
    thread_starter()
