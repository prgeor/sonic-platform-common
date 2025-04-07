"""
   xcvr_cdb.py

   CDB Message handler
"""

import time
from .fields import cdb_consts
from .xcvr_eeprom import XcvrEeprom

#TODO rename CdbCmdHandler
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
        delay = cdb_consts.CDB_MAX_ACCESS_HOLD_OFF_PERIOD // cdb_consts.CDB_MAX_CAPTURE_TIME
        while (delay > 0):
            time.sleep(cdb_consts.CDB_MAX_CAPTURE_TIME // 1000)
            delay -= 1
            status = self.read(cdb_consts.CDB1_QUERY_STATUS)
            if status is not None:
                break

        if status is None:
            print("CDB command failed to reply")
            return None

        #status = self.read(cdb_consts.CDB1_CMD_STATUS)
        if status[cdb_consts.CDB1_IS_BUSY] or status[cdb_consts.CDB1_HAS_FAILED]:
            status = self.read(cdb_consts.CDB1_COMMAND_RESULT)
        return status

class CdbFwHandler(CdbMsgHandler):
    def __init__(self, reader, writer, mem_map):
        super(CdbFwHandler, self).__init__(reader, writer, mem_map)
        self.start_payload_size = 0
        self.is_lpl_only = False
        self.rw_length_ext = cdb_consts.LPL_MAX_PAYLOAD_SIZE if self.is_lpl_only \
                                            else cdb_consts.EPL_MAX_PAYLOAD_SIZE

    def write_epl_page(self, page, data):
        """
        Write a page of data to the EPL page
        """
        # Write the data to the specified page and offset
        assert len(data) <= cdb_consts.PAGE_SIZE, \
                                    "Data length exceeds page size"
        assert page >= cdb_consts.EPL_PAGE, \
                    "Page number must be greater than or equal to 0xA0"
        self.write_raw(page * cdb_consts.PAGE_SIZE, len(data), data)

    def start_fw_download(self, imgpath):
        with open(imgpath, 'rb') as fw_file:
            # Read the image file header bytes
            header_data = None
            if self.start_payload_size > 0:
                header_data = fw_file.read(self.start_payload_size)
                if len(header_data) < self.start_payload_size:
                    raise ValueError(f"Firmware image file is too small < \
                                        {self.start_payload_size} bytes for header")

        # Verify the header with the module
        payload = {
            "imgsize" : len(header_data),
            "imghdr" : header_data
        }
        # Send the CDB start firmware download command
        self.write_cmd(cdb_consts.CDB_START_FIRMWARE_DOWNLOAD_CMD, payload)
        time.sleep(2)
        # Check the status of the command
        status = self.get_status()
        print(f"Start firmware download status: {status}")

    def run_fw_image(self, runmode=0x2, resetdelay=2):
        """
        Run the firmware image
        :param runmode: 0x0: run the image, 0x1: 
        reset the module, 0x2: run and reset        
        """
        payload = {
            "runmode" : runmode,
            "delay" : resetdelay
        }
        # Send the CDB run firmware image command
        self.write_cmd(cdb_consts.CDB_START_FIRMWARE_DOWNLOAD_CMD, payload)
        time.sleep(3)
        status = self.get_status()
        print(f"Run firmware image status: {status}")

    def commit_fw_image(self):
        self.write_cmd(cdb_consts.CDB_COMMIT_FIRMWARE_IMAGE_CMD)
        status = self.get_status()
        print(f"Commit firmware image status: {status}")

    def abort_fw_download(self):
        self.write_cmd(cdb_consts.CDB_ABORT_FIRMWARE_DOWNLOAD_CMD)
        status = self.get_status()
        print(f"Abort firmware download status: {status}")

    def write_lpl_block(self, blkaddr, blkdata):
        """
        Write LPL block
        """
        payload = {
            "blkaddr" : blkaddr,
            "blkdata" : blkdata
        }
        # Send the CDB write firmware LPL command
        self.write_cmd(cdb_consts.CDB_WRITE_FIRMWARE_LPL_CMD, payload)
        status = self.get_status()
        print(f"Write LPL block status: {status}")

    def write_epl_pages(self, blkdata):
        """
        Write EPL pages starting from page 0xA0
        """
        pages = len(blkdata) // cdb_consts.PAGE_SIZE
        assert pages <= cdb_consts.EPL_MAX_PAGES, "Data exceeds maximum number of EPL pages"

        for page in range(pages):
            page_data = blkdata[page * cdb_consts.PAGE_SIZE : (page + 1) * cdb_consts.PAGE_SIZE]
            self.write_epl_page(page + cdb_consts.EPL_PAGE, page_data)

        # Handle any remaining data that doesn't fit into a full page
        if len(blkdata) % cdb_consts.PAGE_SIZE != 0:
            remaining_data = blkdata[pages * cdb_consts.PAGE_SIZE:]
            self.write_epl_page(pages + cdb_consts.EPL_PAGE, remaining_data)

    def write_epl_block(self, blkaddr, blkdata):
        """
        Write EPL block
        """
        payload = {
            "blkaddr" : blkaddr,
            "blkdata" : blkdata
        }
        # Send the CDB write firmware EPL command
        self.write_cmd(cdb_consts.CDB_WRITE_FIRMWARE_EPL_CMD, payload)
        status = self.get_status()
        print(f"Write EPL block status: {status}")

    def download_fw_image(self, imgpath):
        """
        Download firmware image
        :param imgpath: path to the firmware image
        """
        try:
            with open(imgpath, 'rb') as fw_file:
                # Step 1. Read the initial payload (header)
                header_data = None
                if self.start_payload_size > 0:
                    header_data = fw_file.read(self.start_payload_size)
                    if len(header_data) < self.start_payload_size:
                        raise ValueError(f"Firmware image file is too small: \
                                         expected at least {self.start_payload_size} bytes for header")

                # 2 Read and write firmware data in chunks, handling partial chunks
                blkaddr = 0
                while True:
                    # Read a chunk of data up to self.rw_length_ext bytes
                    blkdata = fw_file.read(self.rw_length_ext)

                    # Exit loop if no more data
                    if not blkdata:
                        break

                    # TODO Handle LPL only supported case
                    # TODO Handle auto paging for EPL
                    # Write the block data to the EPL
                    if self.is_lpl_only:
                        self.write_lpl_block(blkaddr, blkdata)
                    else:
                        self.write_epl_block(blkaddr, blkdata)

                    # Update address for next chunk by the actual number of bytes written
                    blkaddr += len(blkdata)

                return True, blkaddr  # Return success and total bytes written

        except FileNotFoundError:
            print(f"Error: Firmware image file not found: {imgpath}")
            return False, 0
        except ValueError as ve:
            print(f"Error: {str(ve)}")
            return False, 0
        except Exception as e:
            print(f"Error downloading firmware image: {str(e)}")
            self.abort_fw_download()  # Abort on error
        return False, 0
