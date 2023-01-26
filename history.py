from lru import LRU

HISTORY = LRU(50)

def appendHistory(ts, msg):
    if HISTORY.has_key(ts):
        conversations = HISTORY[ts]+ "\n"+ msg
    else:
        conversations = msg
    HISTORY[ts] = conversations

def retrieveHistory(ts):
    return HISTORY[ts]
