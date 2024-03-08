from run import app
from flask import g
import time 


@app.before_request
def before_request():
    g.request_start_time = time.time()

@app.after_request
def after_request(r):
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    print("Elapse time  = "+ str(g.request_time()))
    return r 


