"""
   xcvr_cdb.py

   CDB Message handler
"""

from .fields import cdb_consts
from .xcvr_eeprom import XcvrEeprom

class CdbMsgHandler(XcvrEeprom):
    def __init__(self, reader, writer, mem_map):
        super(CdbMsgHandler, self).__init__(reader, writer, mem_map)

    def read_reply(self, cdb_cmd_id):
        """
        Read a reply from the CDB
        """
        cdb_cmd = self.mem_map.get_cdb_cmd(cdb_cmd_id)
        reply_field = cdb_cmd.get_reply_field()
        if reply_field is not None:
            return self.read(reply_field)
        return None
    
    def write_cmd(self, cdb_cmd_id, payload=None):
        """
        Write CDB command
        """
        cdb_cmd = self.mem_map.get_cdb_cmd(cdb_cmd_id)
        if payload is not None:
            bytes = cdb_cmd.encode(payload)
        else:
            bytes = cdb_cmd.encode()
        # TODO Check the module capability CdbCommandTriggerMethod to write in single I2C transaction
        # Write the bytes starting from the 3rd byte(0x9F:130)
        self.writer(cdb_cmd.getaddr() + 2, len(bytes) - 2, bytes[2:])
        # Finally write the first two CMD bytes to trigger CDB processing
        return self.writer(cdb_cmd.getaddr(), 2, bytes[:2])
    
    def get_status(self):
        """
        Get the status of the last CDB command
        Returns None if Module failed to reply to I2C command
        """
        status = self.read(cdb_consts.CDB1_CMD_STATUS)
        if status is not None:
            if status[cdb_consts.CDB1_IS_BUSY] or status[cdb_consts.CDB1_HAS_FAILED]:
                status = self.read(cdb_consts.CDB1_COMMAND_RESULT)
        return status
    


