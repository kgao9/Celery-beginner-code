#variety of different tasks used to experiment with celery
#testing to see exactly how it might interface with GUP
#WARNING: these are mocks with a bunch of details abstracted - they
#don't mirror the internals of the functions at all 

from celery import Celery
import celery
from time import sleep
import subprocess

class additionNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toJSON(self):
        return {'x': self.x, 'y': self.y}

#app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')

#rpc doesn't work with chords... Had to use amqp
app = Celery('tasks', backend='amqp://', broker='pyamqp://guest@localhost//')
class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

'''
param is just a value

This is just going to help mock a
pipelined calculation
'''

def echo_output(param, fname):
    sleep(30)
    
    f = open(fname, 'w')

    p = ''

    #only prints out success, warning, or failure
    if(param > 0):
        p = subprocess.Popen("echo success", shell=True, stdout=f)
    elif(param == 0):
        p = subprocess.Popen("echo warning", shell=True, stdout=f)
    else:
        p = subprocess.Popen("echo failure", shell=True, stdout=f)
    p.wait()

    assert(p.returncode == 0)

    f.close()
    
@app.task
def get_result(fname):
    #perhaps did_fail would be a better name?
    f = open(fname, 'r')

    string = f.next()

    if(string != "failure\n"):
        f.close()
        return 0

    f.close()

    return -1

#2 of the calculations we do in the pipeline...
#if we can make 2 work, the rest should just mimic this
#Might want better names like task_one, task_two... Might be better
#because it shows a before after result? Open to suggestions for sure
@app.task
def bcl(param):
    #technically will have race conditions if multiple of these procs
    #but for the purpose of this interface, I'll assume that bug isn't there
    #BTW fnames should be unique to avoid this race condition - but I want
    # this tutorial to be easily removed, so... WE'll ignore it.
    echo_output(param, "bcl_result.txt")
    res = get_result("bcl_result.txt")
    return res

@app.task
def fastq(callBack, param):
    print "printing callBack"
    print callBack
    if(callBack <= -1):
        return -1

    echo_output(param + callBack, "fastq_result.txt")

    return get_result("fastq_result.txt")

#this is for chords
#callback is result of multiple bcl calcs
@app.task
def fastq_mult(callback, param):
    print(callback)
    if -1 not in callback:
        echo_output(param, "fastq_result.txt")

        return get_result("fastq_result.txt")

    return -1

#tutorial code
@app.task
def add(x,y):
    sleep(60)
    return x + y

@app.task(base=MyTask)
def err(x,y):
    if(x+y == 8):
        raise KeyError()
 
    return x+y

#try to add objects
#had to use a workaround
#celery doesn't like objects, still in beta version mode on that
@app.task
def addObj(dic):
    sleep(5)

    myNode = additionNode(dic['x'], dic['y'])
    return myNode.x + myNode.y
