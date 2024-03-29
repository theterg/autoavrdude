from subprocess import Popen, PIPE
import threading
import fcntl
import os
import Queue

def setNonBlocking(fd):
    """
    Set the file description of the given file descriptor to non-blocking.
    """
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

def reader(fd, queue):
    while True:
        try:
            data = fd.read()
            queue.put(data)
        except IOError:
            continue
        except Exception:
            return

def flushAndWrite(msg, p):
    p.stdout.flush()
    p.stderr.flush()
    p.stdin.write(msg)
    p.stdin.flush()

def writeAndReadResponse(msg, infd, outfd):
    outfd.flush()
    infd.write(msg)
    infd.flush()
    while True:
        try:
            return outfd.read()
        except IOError:
            continue
        except KeyboardInterrupt:
            return ''


def getVtarget(msg):
    lines = msg.split('\n')
    for line in lines:
        if line.startswith('Vtarget'):
            return float(line.split(':')[1][:-2])
    return 0.0

p = Popen("avrdude -c avrispmkii -p m328p -P usb -F -t", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
setNonBlocking(p.stdout)
setNonBlocking(p.stderr)

#outqueue = Queue.Queue()
#errqueue = Queue.Queue()
#
#outthread = threading.Thread(target=reader, args=(p.stdout, outqueue))
#errthread = threading.Thread(target=reader, args=(p.stderr, errqueue))
#
#outthread.start()
#errthread.start()

