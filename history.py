from lru import LRU


class ConversationHistory:
    def __init__(self, size=50):
        self.ts_to_history = LRU(size)

    def appendMessage(self, ts, msg):
        if self.ts_to_history.has_key(ts):
            conversations = self.ts_to_history[ts] + [msg]
        else:
            conversations = [msg]
        self.ts_to_history[ts] = conversations

    def retrieveMessages(self, ts, max_length):
        history = self.ts_to_history[ts]
        if history is None:
            return []
        # if history is None or len(history) < 1:
        #     return []

        # Find i such that the concatenation of history[i:] is around the softLimit
        length = 0
        i = len(history)
        for msg in reversed(history):
            length += len(msg)
            if length >= max_length:
                break
            i -= 1
        i = min(i, len(history) - 1)
        return history[i:]
