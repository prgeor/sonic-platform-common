"""
   xcvr_cdb.py

   CDB Message instance handler for Xcvr
"""

import struct

class XcvrCdbMsg(object):
    def __init__(self, reader, writer, mem_map):
        self.reader = reader
        self.writer = writer
        self.mem_map = mem_map

    def read_reply(self, cdb_cmd):
        """
        Read a reply from the CDB
        """
        raw_data = self.reader(0x0, 1)
        if raw_data:
            return struct.unpack("B", raw_data)[0]
        return None
    

    def write_cmd(self, cdb_cmd):
        """
        Write a command to the CDB
        """
        self.writer(0x0, struct.pack("B", cdb_cmd))
        return True
    
    def get_status(self, cdb_cmd):
        """
        Get the status of a CDB command
        """
        self.write_cmd(cdb_cmd)
        return self.read_reply(cdb_cmd)
    


