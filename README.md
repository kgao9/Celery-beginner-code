just a little tutorial on celery

I only have a basic interface with chord and chain working, but
it does work asynchronously with only 1-2 race conditions, so...

Oh I should mention - the race condition is intentional and documented.

Not bad for a day of programming...

Hopefully, I can create a DAG one day...

To run, in the command line, run "celery -A tasks worker --loglevel=info" and then in another terminal run "python main.py"
