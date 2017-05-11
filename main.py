from tasks import bcl, fastq, fastq_mult
from celery import chain, chord
from IPython import embed

def bcl_exec(param):
    proc = bcl.delay(param)
    print proc.get()

def fastq_exec_chain(bclParam, fastqParam):
    sig = bcl.s(bclParam)

    #simply put, executes sig (bcl) first then fastq
    #but this is assuming params are passed in sequence that is
    #there is nothing in terms of multiple threads - pretty bad seeing
    #as how we'rd multiplexing stuff...
    #hmmm... We'll need to use chords but how do I abstract that out?
    #something to think about
    res = chain(sig, fastq.s(fastqParam))()
    print res.get()

#bclParam is a list
def fastq_exec_chord(bclParam, fastqParam):
    sig_list = []

    print bclParam

    for param in bclParam:
        sig_list.append(bcl.s(param))

    print sig_list

    res = chord(sig_list)(fastq_mult.s(fastqParam))
    print res.get()

getRange = [i for i in xrange(10)]
#getRange = [-1]
#getRange.append(-1) 
print(getRange)
fastq_exec_chord(getRange, 10)

#fastq_exec_chain(-1, 10)

