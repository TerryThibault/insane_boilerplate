import socket
import pickle
import thread

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
    thread.start_new_thread(start, (param1, param2))

def start(param1, param2):
    ## do something

if __name__ == '__main__':
    thread_starter()
