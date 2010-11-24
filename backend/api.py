
from parser import FileParser

class LogLine(object):
    """
    Basic object that represents a log line; pass in the timestamp
    and stream name and it will extract the right bits of data and
    make them accessible via attributes.
    """
    
    def __init__(self, redis_conn, stream_name, timestamp):
        self.redis_conn = redis_conn
        self.stream_name = stream_name
        self.timestamp = timestamp
        self._load()

    @classmethod
    def by_log_line_id(cls, redis_conn, log_line_id):
        stream, timestamp = log_line_id.split(":", 1)
        timestamp = int(timestamp)
        return cls(redis_conn, stream, timestamp)

    def _load(self):
        # Load the file parser
        fp = FileParser(self.stream_name)
        # Find the offset and load just one item from there
        offset = self.redis_conn.get("stream:%s:%i:offset" % (self.stream_name, self.timestamp))
        item = iter(fp.get_chunks(int(offset))).next()
        # Load onto our attributes
        self.lines = item['lines']

    def __str__(self):
        return "<LogLine %s:%i (%s lines)>" % (self.stream_name, self.timestamp, len(self.lines))
    
class Query(object):
    """
    Query interface to LogLines.
    """

    def __init__(self):
        pass

