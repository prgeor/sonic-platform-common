
from ...fields import cdb_consts
from ..xcvr_mem_map import XcvrMemMap

from ...fields.xcvr_field import (
    XcvrField,
    CodeRegField,
    DateField,
    HexRegField,
    NumberRegField,
    RegBitField,
    RegBitsField,
    RegGroupField,
    StringRegField,
)

from ...fields.public.cmis import CdbStatusField

import struct

class CdbMemMap(XcvrMemMap):
    def __init__(self, codes):
        super(CdbMemMap, self).__init__(codes)

        self.query_status = CodeRegField(cdb_consts.CDB1_QUERY_STATUS,
                                            self.getaddr(cdb_consts.LPL_PAGE, 137),
                                            self.codes.CDB_QUERY_STATUS)

        self.cdb1_status = RegGroupField(cdb_consts.CDB1_CMD_STATUS_FIELD,
            NumberRegField(cdb_consts.CDB1_CMD_STATUS, self.getaddr(0x0, 37),
                RegBitField(cdb_consts.CDB1_IS_BUSY, 7),
                RegBitField(cdb_consts.CDB1_HAS_FAILED, 6)),
                RegBitsField(cdb_consts.CDB1_STATUS, bitpos=0, size=6),
            CdbStatusField(cdb_consts.CDB1_COMMAND_RESULT, self.getaddr(0x0, 37), size=1, format="B",
                           deps=[(cdb_consts.CDB1_IS_BUSY, cdb_consts.CDB1_HAS_FAILED)]),
        )

        self.cdb1_firmware_info = RegGroupField(cdb_consts.CDB1_FIRMWARE_INFO,
                NumberRegField(cdb_consts.CDB1_FIRMWARE_STATUS, self.getaddr(cdb_consts.LPL_PAGE, 136),
                    RegBitField(cdb_consts.CDB1_BANKA_OPER_STATUS, 0),
                    RegBitField(cdb_consts.CDB1_BANKB_OPER_STATUS, 4),
                    RegBitField(cdb_consts.CDB1_BANKA_ADMIN_STATUS, 1),
                    RegBitField(cdb_consts.CDB1_BANKB_ADMIN_STATUS, 5),
                    RegBitField(cdb_consts.CDB1_BANKA_VALID_STATUS, 2),
                    RegBitField(cdb_consts.CDB1_BANKB_VALID_STATUS, 6)),
                NumberRegField(cdb_consts.CDB1_IMAGE_INFO, self.getaddr(cdb_consts.LPL_PAGE, 137),
                               RegBitField(cdb_consts.CDB1_IMAGEA_VERSION_PRESENT, 0),
                               RegBitField(cdb_consts.CDB1_IMAGEB_VERSION_PRESENT, 1),
                               RegBitField(cdb_consts.CDB1_FACTIMG_VERSION_PRESENT, 2)),
                NumberRegField(cdb_consts.CDB1_BANKA_MAJOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 138), size=1),
                NumberRegField(cdb_consts.CDB1_BANKA_MINOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 139), size=1),
                NumberRegField(cdb_consts.CDB1_BANKA_BUILD_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 140), size=2),
                NumberRegField(cdb_consts.CDB1_BANKB_MAJOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 174), size=1),
                NumberRegField(cdb_consts.CDB1_BANKB_MINOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 175), size=1),
                NumberRegField(cdb_consts.CDB1_BANKB_BUILD_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 176), size=2),
                NumberRegField(cdb_consts.CDB1_FACTORY_MAJOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 210), size=1),
                NumberRegField(cdb_consts.CDB1_FACTORY_MINOR_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 211), size=1),
                NumberRegField(cdb_consts.CDB1_FACTORY_BUILD_VERSION, self.getaddr(cdb_consts.LPL_PAGE, 212), size=2),
        )

    def getaddr(self, page, offset, page_size=128):
        return page * page_size + offset

class CDBCommand():
    """
    Custom CDB command field.

    Args:
        id: 2 bytes identifier
        epl: 2 bytes extended payload length
        lpl: 1 byte length of payload
        checksum: 1 byte checksum
    """
    def __init__(self, name, cmd_id=0, epl=0, lpl=0, payload=None, rpl_field=None):
        self.name = name
        self.id = cmd_id
        self.epl = epl
        self.lpl = lpl
        self.rpl = struct.pack(">H", 0)
        self.page = 0x9F
        self.offset = 128
        self.rpl_field = rpl_field
        self.payload = payload
        assert self.epl >= 0 and self.epl < 2047, "epl must be between 0 and 2048"
        assert self.lpl >= 0 and self.lpl < 256, "lpl must be between 0 and 256"

    def get_reply_field(self):
        return self.rpl_field
    
    def checksum(self, data):
        '''
        Returns checksum of the CDB command
        '''
        cksum = 0
        for byte in data:
            cksum += byte
        return 0xff - (cksum & 0xff)

    def getaddr(self):
        return (self.page * 128) + self.offset

    def get_size(self):
        return 6  # 2 bytes for id, 2 bytes for epl, 1 byte for lpl, 1 byte for checksum
    
    def encode(self):
        """
        Encodes the CDB command(hdr+payload) into bytes
        """
        id_bytes = struct.pack(">H", self.id)
        epl_bytes = struct.pack(">H", self.epl)
        lpl_byte = struct.pack("B", self.lpl)
        hdr_bytes = id_bytes + epl_bytes + lpl_byte
        if self.payload is not None:
            cksum = self.checksum(hdr_bytes + self.payload)
        else:
            cksum = self.checksum(hdr_bytes)
        cmd_bytes = hdr_bytes + cksum + self.rpl 
        if self.payload is not None:
            cmd_bytes = cmd_bytes + self.payload
        return cmd_bytes 

    def decode(self, raw_data):
        id = struct.unpack(">H", raw_data[:2])[0]
        epl = struct.unpack(">H", raw_data[2:4])[0]
        lpl = struct.unpack("B", raw_data[4:5])[0]
        checksum = struct.unpack("B", raw_data[5:6])[0]
        rpl = struct.unpack(">H", raw_data[6:8])[0]
        delay = struct.unpack("H", raw_data[8:10])[0]
        return {
            "id": id,
            "epl": epl,
            "lpl": lpl,
            "checksum": checksum,
            "rpl": rpl,
            "delay": delay
        }

class CdbStatusQuery(CDBCommand):
    """
    Custom CDB command field.

    Args:
        id: 2 bytes identifier
        epl: 2 bytes extended payload length
        lpl: 1 byte length of payload
        checksum: 1 byte checksum
    """
    def __init__(self, name="CdbQueryStatus", cmd_id=cdb_consts.CDB_QUERY_STATUS_CMD,
                 reply_field=cdb_consts.CDB1_QUERY_STATUS):
        super(CdbStatusQuery, self).__init__(name,
                                            cmd_id,
                                            epl=0,
                                            lpl=2,
                                            payload=struct.pack(">H", 0x0010),
                                            rpl_field=reply_field)

class CdbGetFirmwareInfo(CDBCommand):
    """
    Custom CDB command field.

    Args:
        id: 2 bytes identifier
        epl: 2 bytes extended payload length
        lpl: 1 byte length of payload
        checksum: 1 byte checksum
    """
    def __init__(self, name="CdbGetFirmwareInfo", cmd_id=cdb_consts.CDB_GET_FIRMWARE_INFO_CMD,
                 reply_field=cdb_consts.CDB1_FIRMWARE_INFO):
        super(CdbGetFirmwareInfo, self).__init__(name,
                                            cmd_id,
                                            epl=0,
                                            lpl=0,
                                            payload=None,
                                            rpl_field=reply_field)