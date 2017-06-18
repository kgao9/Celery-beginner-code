just a little tutorial on celery

I only have a basic interface with chord and chain working, but
it does work asynchronously with only 1-2 race conditions, so...

Oh I should mention - the race condition is intentional and documented - can be fixed using python's lockfile module except I have lost access to a linux computer with celery, so if I do fix it, I cannot retest to see if it works so I'm leaving the issue here with a note :'(.

Not bad for a day of programming...

Hopefully, I can create a DAG one day...

To run, in the command line, run "celery -A tasks worker --loglevel=info" and then in another terminal run "python main.py"
