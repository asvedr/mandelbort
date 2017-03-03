#!/usr/bin/env python3
import subprocess as sp

user = sp.check_output(['whoami']).decode().strip()
tbl = sp.check_output(['ps', '-u' , user]).decode()
lines = tbl.split('\n')[1:]
process = []
for line in lines:
    acc = []
    for word in line.split(' '):
        if len(word) > 0:
            acc.append(word)
    if len(acc) > 0:
        process.append(acc)
# now we have process table like
# [[PID, TTY, TIME, CMD] ... ] in 'process'
# killing first uwsgi proc
def killProc():
    for proc in process:
        if proc[3] == 'uwsgi':
            try:
                sp.check_output(['kill', '-9' ,proc[0]])
                return 'ok: %s' % proc[0]
            except:
                print("can't kill %s" % proc)
    return 'not found'

print(killProc())
