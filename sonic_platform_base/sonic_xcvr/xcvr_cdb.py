"""
   xcvr_cdb.py

   CDB Message handler
"""

import sonic_xcvr.fields.cdb_consts as cdb_consts
from .xcvr_eeprom import XcvrEeprom

class XcvrCdbHandler(XcvrEeprom):
    def __init__(self, reader, writer, mem_map):
        super(XcvrCdbHandler, self).__init__(reader, writer, mem_map)

    def read_reply(self, cdb_cmd):
        """
        Read a reply from the CDB
        """
        reply_field = cdb_cmd.get_reply_field()
        if reply_field is not None:
            return self.read(reply_field)
        return None
    
    def write_cmd(self, cdb_cmd):
        """
        Write CDB command
        """
        bytes = cdb_cmd.encode()
        # TODO Check the module capability CdbCommandTriggerMethod to write in single I2C transaction
        # Write the bytes starting from the 3rd byte(0x9F:130)
        self.writer(cdb_cmd.get_offset() + 2, len(bytes) - 2, bytes[2:])
        # Finally write the first two CMD bytes to trigger CDB processing
        return self.writer(cdb_cmd.get_offset(), 2, bytes[:2])
    
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
    


