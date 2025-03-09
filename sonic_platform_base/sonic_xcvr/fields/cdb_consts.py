
#CDB Related
CDB1_QUERY_STATUS = "Cdb1QueryStatus"
CDB1_STATUS = "Cdb1Status"
CDB1_CMD_STATUS = "Cdb1CmdStatus"
CDB1_IS_BUSY = "Cdb1IsBusy"
CDB1_HAS_FAILED = "Cdb1HasFailed"
CDB1_CMD_STATUS_FIELD = "Cdb1CmdStatus"
CDB1_COMMAND_RESULT ="Cdb1CommandResult"


#Firmware Info
CDB1_FIRMWARE_INFO = "Cdb1FirmwareInfo"
CDB1_FIRMWARE_STATUS = "Cdb1FirmwareStatus"
CDB1_BANKA_OPER_STATUS = "CdbBankAOperStatus"
CDB1_BANKB_OPER_STATUS = "CdbBankBOperStatus"
CDB1_BANKA_ADMIN_STATUS = "CdbBankAAdminStatus"
CDB1_BANKB_ADMIN_STATUS = "CdbBankBAdminStatus"
CDB1_BANKA_VALID_STATUS = "CdbBankAValidStatus"
CDB1_BANKB_VALID_STATUS = "CdbBankBValidStatus"
CDB1_IMAGE_INFO = "CdbImageInfo"
CDB1_FIRMWARE_VERSION = "Cdb1FirmwareVersion"
CDB1_BANKA_IMAGE_VERSION = "CdbBankAImageVersion"
CDB1_BANKB_IMAGE_VERSION = "CdbBankBImageVersion"
CDB1_BANKA_MAJOR_VERSION = "CdbBankAMajorVersion"
CDB1_BANKB_MAJOR_VERSION = "CdbBankBMajorVersion"
CDB1_BANKA_MINOR_VERSION = "CdbBankAMinorVersion"
CDB1_BANKB_MINOR_VERSION = "CdbBankBMinorVersion"
CDB1_BANKA_BUILD_VERSION = "CdbBankABuildVersion"
CDB1_BANKB_BUILD_VERSION = "CdbBankBBuildVersion"
CDB1_FACTORY_MAJOR_VERSION = "CdbFactoryMajorVersion"
CDB1_FACTORY_MINOR_VERSION = "CdbFactoryMinorVersion"
CDB1_FACTORY_BUILD_VERSION = "CdbFactoryBuildVersion"
CDB1_IMAGEA_VERSION_PRESENT = "CdbImageAVersionPresent"
CDB1_IMAGEB_VERSION_PRESENT = "CdbImageBVersionPresent"
CDB1_FACTIMG_VERSION_PRESENT = "CdbFactoryImgVersionPresent"


LPL_PAGE = 0x9F
RPL_DATA_START_OFFSET = 136
LPL_MAX_PAYLOAD_SIZE = 120
EPL_MAX_PAYLOAD_SIZE = 2048

#CDB Commands
CDB_CMD_ID_LEN = 2
CDB_QUERY_STATUS_CMD = 0x0000
CDB_ENTER_PASSWORD_CMD = 0x0001
CDB_CHANGE_PASSWORD_CMD = 0x0002
CDB_ABORT_CMD = 0x0003
CDB_MODULE_FEATURE_CMD= 0x0004
CDB_GET_FIRMWARE_INFO_CMD = 0x0100
