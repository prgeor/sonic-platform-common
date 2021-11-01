"""
    cmis.py

    Implementation of XcvrMemMap for CMIS Rev 5.0
"""

from ..xcvr_mem_map import XcvrMemMap
from ...fields.xcvr_field import (
    CodeRegField,
    DateField,
    HexRegField,
    NumberRegField,
    RegBitField,
    RegGroupField,
    StringRegField,
)
from ...fields import consts
from ...fields.public.cmis import CableLenField

class CmisMemMap(XcvrMemMap):
    def __init__(self, codes):
        super(CmisMemMap, self).__init__(codes)

        self.MGMT_CHARACTERISTICS = RegGroupField(consts.MGMT_CHAR_FIELD,
            NumberRegField(consts.MGMT_CHAR_MISC_FIELD, self.getaddr(0x0, 2),
                RegBitField(consts.FLAT_MEM_FIELD, 7)
            )
        )

        self.ADMIN_INFO = RegGroupField(consts.ADMIN_INFO_FIELD,
            CodeRegField(consts.ID_FIELD, self.getaddr(0x0, 128), self.codes.XCVR_IDENTIFIERS),
            StringRegField(consts.VENDOR_NAME_FIELD, self.getaddr(0x0, 129), size=16),
            HexRegField(consts.VENDOR_OUI_FIELD, self.getaddr(0x0, 145), size=3),
            StringRegField(consts.VENDOR_PART_NO_FIELD, self.getaddr(0x0, 148), size=16),
            StringRegField(consts.VENDOR_REV_FIELD, self.getaddr(0x0, 164), size=2),
            StringRegField(consts.VENDOR_SERIAL_NO_FIELD, self.getaddr(0x0, 166), size=16),
            DateField(consts.VENDOR_DATE_FIELD, self.getaddr(0x0, 182), size=8),
            RegGroupField(consts.EXT_ID_FIELD,
                CodeRegField(consts.POWER_CLASS_FIELD, self.getaddr(0x0, 200), self.codes.POWER_CLASSES,
                    *(RegBitField("%s_%d" % (consts.POWER_CLASS_FIELD, bit), bit) for bit in range(5, 8))
                ),
                NumberRegField(consts.MAX_POWER_FIELD, self.getaddr(0x0, 201), scale=4),
            ),
            NumberRegField(consts.LEN_MULT_FIELD, self.getaddr(0x0, 202),
                *(RegBitField("%s_%d" % (consts.LEN_MULT_FIELD, bit), bit) for bit in range (6, 8))
            ),
            CableLenField(consts.LENGTH_ASSEMBLY_FIELD, self.getaddr(0x0, 202),
                *(RegBitField("%s_%d" % (consts.LENGTH_ASSEMBLY_FIELD, bit), bit) for bit in range(0, 6))
            ),

            CodeRegField(consts.CONNECTOR_FIELD, self.getaddr(0x0, 203), self.codes.CONNECTORS,
                deps=[consts.LEN_MULT_FIELD]
            ),
            CodeRegField(consts.HOST_ELECTRICAL_INTERFACE, self.getaddr(0x0, 86), self.codes.HOST_ELECTRICAL_INTERFACE),
            CodeRegField(consts.MEDIA_TYPE_FIELD, self.getaddr(0x0, 85), self.codes.MODULE_MEDIA_TYPE),
            CodeRegField(consts.MODULE_MEDIA_INTERFACE_850NM, self.getaddr(0x0, 87), self.codes.NM_850_MEDIA_INTERFACE),
            CodeRegField(consts.MODULE_MEDIA_INTERFACE_SM, self.getaddr(0x0, 87), self.codes.SM_MEDIA_INTERFACE),
            CodeRegField(consts.MODULE_MEDIA_INTERFACE_PASSIVE_COPPER, self.getaddr(0x0, 87), self.codes.PASSIVE_COPPER_MEDIA_INTERFACE),
            CodeRegField(consts.MODULE_MEDIA_INTERFACE_ACTIVE_CABLE, self.getaddr(0x0, 87), self.codes.ACTIVE_CABLE_MEDIA_INTERFACE),
            CodeRegField(consts.MODULE_MEDIA_INTERFACE_BASE_T, self.getaddr(0x0, 87), self.codes.BASE_T_MEDIA_INTERFACE),
            NumberRegField(consts.LANE_COUNT, self.getaddr(0x0, 88), format="B", size=1),
            NumberRegField(consts.HOST_LANE_ASSIGNMENT_OPTION, self.getaddr(0x0, 89), format="B", size=1),
            NumberRegField(consts.MEDIA_LANE_ASSIGNMENT_OPTION, self.getaddr(0x1, 176), format="B", size=1),
            CodeRegField(consts.MEDIA_INTERFACE_TECH, self.getaddr(0x0, 212), self.codes.MEDIA_INTERFACE_TECH),
            NumberRegField(consts.HW_MAJOR_REV, self.getaddr(0x1, 130), size=1),
            NumberRegField(consts.HW_MINOR_REV, self.getaddr(0x1, 131), size=1),
            NumberRegField(consts.CMIS_REVISION, self.getaddr(0x0, 1), format="B", size=1),
            NumberRegField(consts.ACTIVE_FW_MAJOR_REV, self.getaddr(0x0, 39), format="B", size=1),
            NumberRegField(consts.ACTIVE_FW_MINOR_REV, self.getaddr(0x0, 40), format="B", size=1),
            NumberRegField(consts.INACTIVE_FW_MAJOR_REV, self.getaddr(0x1, 128), format="B", size=1),
            NumberRegField(consts.INACTIVE_FW_MINOR_REV, self.getaddr(0x1, 129), format="B", size=1),

            RegGroupField(consts.ACTIVE_APSEL_CODE,
                *(NumberRegField("%s%d" % (consts.ACTIVE_APSEL_HOSTLANE, lane) , self.getaddr(0x11, offset),
                    *(RegBitField("Bit%d" % bit, bit) for bit in range(0, 4)))
                 for lane, offset in zip(range(1, 9), range(206, 214)))
            )
        )

        self.MODULE_LEVEL_MONITORS = RegGroupField(consts.MODULE_MONITORS_FIELD,
            NumberRegField(consts.TEMPERATURE_FIELD, self.getaddr(0x0, 14), size=2, format=">h", scale=256),
            NumberRegField(consts.VOLTAGE_FIELD, self.getaddr(0x0, 16), size=2, format=">H", scale=10000),
            NumberRegField(consts.TX_POW, self.getaddr(0x11, 154), format=">H", size=2, scale=10000.0),
            NumberRegField(consts.RX_POW, self.getaddr(0x11, 186), format=">H", size=2, scale=10000.0),
            NumberRegField(consts.TX_BIAS, self.getaddr(0x11, 170), format=">H", size=2, scale=500.0),
            NumberRegField(consts.GRID_SPACING, self.getaddr(0x12, 128), size=1, ro=False),
            NumberRegField(consts.LASER_CONFIG_CHANNEL, self.getaddr(0x12, 136), format=">h", size=2, ro=False),
            NumberRegField(consts.LASER_CURRENT_FREQ, self.getaddr(0x12, 168), format=">L", size=4),
            NumberRegField(consts.TX_CONFIG_POWER, self.getaddr(0x12, 200), format=">h", size=2, scale=100.0, ro=False),
            NumberRegField(consts.AUX_MON_TYPE, self.getaddr(0x1, 145), size=1),
            NumberRegField(consts.AUX1_MON, self.getaddr(0x0, 18), format=">h", size=2),
            NumberRegField(consts.AUX2_MON, self.getaddr(0x0, 20), format=">h", size=2),
            NumberRegField(consts.AUX3_MON, self.getaddr(0x0, 22), format=">h", size=2),
            NumberRegField(consts.CUSTOM_MON, self.getaddr(0x0, 24), format=">H", size=2),
)

        self.MODULE_CHAR_ADVT = RegGroupField(consts.MODULE_CHAR_ADVT_FIELD,
            NumberRegField(consts.CTRLS_ADVT_FIELD, self.getaddr(0x1, 155),
                RegBitField(consts.TX_DISABLE_SUPPORT_FIELD, 1),
                size=2, format="<H"
            ),
            NumberRegField(consts.FLAGS_ADVT_FIELD, self.getaddr(0x1, 157),
                RegBitField(consts.TX_FAULT_SUPPORT_FIELD, 0),
                size=2, format="<H"
            )
        )

        self.THRESHOLDS = RegGroupField(consts.THRESHOLDS_FIELD,
            NumberRegField(consts.TEMP_HIGH_ALARM_FIELD, self.getaddr(0x2, 128), size=2, format=">h", scale=256),
            NumberRegField(consts.TEMP_LOW_ALARM_FIELD, self.getaddr(0x2, 130), size=2, format=">h", scale=256),
            NumberRegField(consts.TEMP_HIGH_WARNING_FIELD, self.getaddr(0x2, 132), size=2, format=">h", scale=256),
            NumberRegField(consts.TEMP_LOW_WARNING_FIELD, self.getaddr(0x2, 134), size=2, format=">h", scale=256),
            NumberRegField(consts.VOLTAGE_HIGH_ALARM_FIELD, self.getaddr(0x2, 136), size=2, format=">H", scale=10000),
            NumberRegField(consts.VOLTAGE_LOW_ALARM_FIELD, self.getaddr(0x2, 138), size=2, format=">H", scale=10000),
            NumberRegField(consts.VOLTAGE_HIGH_WARNING_FIELD, self.getaddr(0x2, 140), size=2, format=">H", scale=10000),
            NumberRegField(consts.VOLTAGE_LOW_WARNING_FIELD, self.getaddr(0x2, 142), size=2, format=">H", scale=10000),
            NumberRegField(consts.TX_POWER_HIGH_ALARM_FIELD, self.getaddr(0x2, 176), size=2, format=">H", scale=1000),
            NumberRegField(consts.TX_POWER_LOW_ALARM_FIELD, self.getaddr(0x2, 178), size=2, format=">H", scale=1000),
            NumberRegField(consts.TX_POWER_HIGH_WARNING_FIELD, self.getaddr(0x2, 180), size=2, format=">H", scale=1000),
            NumberRegField(consts.TX_POWER_LOW_WARNING_FIELD, self.getaddr(0x2, 182), size=2, format=">H", scale=1000),
            NumberRegField(consts.TX_BIAS_HIGH_ALARM_FIELD, self.getaddr(0x2, 184), size=2, format=">H", scale=500),
            NumberRegField(consts.TX_BIAS_LOW_ALARM_FIELD, self.getaddr(0x2, 186), size=2, format=">H", scale=500),
            NumberRegField(consts.TX_BIAS_HIGH_WARNING_FIELD, self.getaddr(0x2, 188), size=2, format=">H", scale=500),
            NumberRegField(consts.TX_BIAS_LOW_WARNING_FIELD, self.getaddr(0x2, 190), size=2, format=">H", scale=500),
            NumberRegField(consts.RX_POWER_HIGH_ALARM_FIELD, self.getaddr(0x2, 192), size=2, format=">H", scale=1000),
            NumberRegField(consts.RX_POWER_LOW_ALARM_FIELD, self.getaddr(0x2, 194), size=2, format=">H", scale=1000),
            NumberRegField(consts.RX_POWER_HIGH_WARNING_FIELD, self.getaddr(0x2, 196), size=2, format=">H", scale=1000),
            NumberRegField(consts.RX_POWER_LOW_WARNING_FIELD, self.getaddr(0x2, 198), size=2, format=">H", scale=1000),
            NumberRegField(consts.AUX1_HIGH_ALARM, self.getaddr(0x2, 144), format=">h", size=2),
            NumberRegField(consts.AUX1_LOW_ALARM, self.getaddr(0x2, 146), format=">h", size=2),
            NumberRegField(consts.AUX1_HIGH_WARN, self.getaddr(0x2, 148), format=">h", size=2),
            NumberRegField(consts.AUX1_LOW_WARN, self.getaddr(0x2, 150), format=">h", size=2),
            NumberRegField(consts.AUX2_HIGH_ALARM, self.getaddr(0x2, 152), format=">h", size=2),
            NumberRegField(consts.AUX2_LOW_ALARM, self.getaddr(0x2, 154), format=">h", size=2),
            NumberRegField(consts.AUX2_HIGH_WARN, self.getaddr(0x2, 156), format=">h", size=2),
            NumberRegField(consts.AUX2_LOW_WARN, self.getaddr(0x2, 158), format=">h", size=2),
            NumberRegField(consts.AUX3_HIGH_ALARM, self.getaddr(0x2, 160), format=">h", size=2),
            NumberRegField(consts.AUX3_LOW_ALARM, self.getaddr(0x2, 162), format=">h", size=2),
            NumberRegField(consts.AUX3_HIGH_WARN, self.getaddr(0x2, 164), format=">h", size=2),
            NumberRegField(consts.AUX3_LOW_WARN, self.getaddr(0x2, 166), format=">h", size=2),
            NumberRegField(consts.SUPPORT_GRID, self.getaddr(0x4, 128)),
            NumberRegField(consts.LOW_CHANNEL, self.getaddr(0x4, 158), format=">h", size=2),
            NumberRegField(consts.HIGH_CHANNEL, self.getaddr(0x4, 160), format=">h", size=2),
            NumberRegField(consts.MIN_PROG_OUTPUT_POWER, self.getaddr(0x4, 198), format=">h", size=2, scale = 100.0),
            NumberRegField(consts.MAX_PROG_OUTPUT_POWER, self.getaddr(0x4, 200), format=">h", size=2, scale = 100.0),
        )

        self.LANE_DATAPATH_CTRL = RegGroupField(consts.LANE_DATAPATH_CTRL_FIELD,
            NumberRegField(consts.TX_DISABLE_FIELD, self.getaddr(0x10, 130), ro=False)
        )

        self.LANE_DATAPATH_STATUS = RegGroupField(consts.LANE_DATAPATH_STATUS_FIELD,
            NumberRegField(consts.TX_FAULT_FIELD, self.getaddr(0x11, 135)),
            NumberRegField(consts.RX_LOS_FIELD, self.getaddr(0x11, 147)),
            RegGroupField(consts.TX_POWER_FIELD,
                *(NumberRegField("OpticalPowerTx%dField" % channel, self.getaddr(0x11, offset), size=2, format=">H", scale=1000)
                for channel, offset in zip(range(1, 9), range(154, 170, 2)))
            ),
            RegGroupField(consts.TX_BIAS_FIELD,
                *(NumberRegField("LaserBiasTx%dField" % channel, self.getaddr(0x11, offset), size=2, format=">H", scale=500)
                for channel, offset in zip(range(1, 9), range(170, 186, 2)))
            ),
            RegGroupField(consts.RX_POWER_FIELD,
                *(NumberRegField("OpticalPowerRx%dField" % channel, self.getaddr(0x11, offset), size=2, format=">H", scale=1000)
                for channel, offset in zip(range(1, 9), range(186, 202, 2)))
            ),

            RegGroupField(consts.DATA_PATH_STATE,
                *(CodeRegField("DP%dState" % (lane) , self.getaddr(0x11, 128 + int(lane/3)), self.codes.DATAPATH_STATE,
                    *(RegBitField("Bit%d" % bit, bit) for bit in [range(4, 8), range(0, 4)][lane%2]))
                 for lane in range(1, 9))
            ),

            NumberRegField(consts.RX_OUTPUT_STATUS, self.getaddr(0x11, 132), size=1),
            NumberRegField(consts.TX_OUTPUT_STATUS, self.getaddr(0x11, 133), size=1),
            NumberRegField(consts.TX_LOS_FLAG, self.getaddr(0x11, 136), size=1),
            NumberRegField(consts.TX_CDR_LOL, self.getaddr(0x11, 137), size=1),
            NumberRegField(consts.TX_POWER_HIGH_ALARM_FLAG, self.getaddr(0x11, 139), size=1),
            NumberRegField(consts.TX_POWER_LOW_ALARM_FLAG, self.getaddr(0x11, 140), size=1),
            NumberRegField(consts.TX_POWER_HIGH_WARN_FLAG, self.getaddr(0x11, 141), size=1),
            NumberRegField(consts.TX_POWER_LOW_WARN_FLAG, self.getaddr(0x11, 142), size=1),
            NumberRegField(consts.TX_BIAS_HIGH_ALARM_FLAG, self.getaddr(0x11, 143), size=1),
            NumberRegField(consts.TX_BIAS_LOW_ALARM_FLAG, self.getaddr(0x11, 144), size=1),
            NumberRegField(consts.TX_BIAS_HIGH_WARN_FLAG, self.getaddr(0x11, 145), size=1),
            NumberRegField(consts.TX_BIAS_LOW_WARN_FLAG, self.getaddr(0x11, 146), size=1),
            NumberRegField(consts.RX_CDR_LOL, self.getaddr(0x11, 148), size=1),
            NumberRegField(consts.RX_POWER_HIGH_ALARM_FLAG, self.getaddr(0x11, 149), size=1),
            NumberRegField(consts.RX_POWER_LOW_ALARM_FLAG, self.getaddr(0x11, 150), size=1),
            NumberRegField(consts.RX_POWER_HIGH_WARN_FLAG, self.getaddr(0x11, 151), size=1),
            NumberRegField(consts.RX_POWER_LOW_WARN_FLAG, self.getaddr(0x11, 152), size=1),
            NumberRegField(consts.CONFIG_LANE_STATUS, self.getaddr(0x11, 202), format=">I", size=4),
            NumberRegField(consts.DPINIT_PENDING, self.getaddr(0x11, 235), size=1),
            RegBitField(consts.TUNING_IN_PROGRESS, offset=self.getaddr(0x12, 222), bitpos=1),
            RegBitField(consts.WAVELENGTH_UNLOCKED, offset=self.getaddr(0x12, 222), bitpos=0),
            NumberRegField(consts.LASER_TUNING_DETAIL, self.getaddr(0x12, 231), size=1),
        )

        self.TRANS_LOOPBACK = RegGroupField(consts.TRANS_LOOPBACK_FIELD,
            NumberRegField(consts.LOOPBACK_CAPABILITY, self.getaddr(0x13, 128), size=1),
            NumberRegField(consts.MEDIA_OUTPUT_LOOPBACK, offset=self.getaddr(0x13, 180), size=1,  ro=False),
            NumberRegField(consts.MEDIA_INPUT_LOOPBACK, offset=self.getaddr(0x13, 181), size=1, ro=False),
            NumberRegField(consts.HOST_OUTPUT_LOOPBACK, self.getaddr(0x13, 182), size=1, ro=False),
            NumberRegField(consts.HOST_INPUT_LOOPBACK, self.getaddr(0x13, 183), size=1, ro=False),
        )

        self.TRANS_MODULE_STATUS = RegGroupField(consts.TRANS_MODULE_STATUS_FIELD,
            CodeRegField(consts.MODULE_STATE, self.getaddr(0x0, 3), self.codes.MODULE_STATE,
                 *(RegBitField("Bit%d" % (bit), bit) for bit in range (1, 4))
            ),
            NumberRegField(consts.MODULE_FIRMWARE_FAULT_INFO, self.getaddr(0x0, 8), size=1),
            NumberRegField(consts.MODULE_FLAG_BYTE1, self.getaddr(0x0, 9), size=1),
            NumberRegField(consts.MODULE_FLAG_BYTE2, self.getaddr(0x0, 10), size=1),
            NumberRegField(consts.MODULE_FLAG_BYTE3, self.getaddr(0x0, 11), size=1),
            NumberRegField(consts.CDB1_STATUS, self.getaddr(0x0, 37), size=1),
            CodeRegField(consts.MODULE_FAULT_CAUSE, self.getaddr(0x0, 41), self.codes.MODULE_FAULT_CAUSE),
        )

        self.TRANS_PM = RegGroupField(consts.TRANS_PM_FIELD,
            NumberRegField(consts.VDM_SUPPORTED_PAGE, self.getaddr(0x2f, 128), size=1, ro=False),
            NumberRegField(consts.VDM_CONTROL, self.getaddr(0x2f, 144), size=1, ro=False),
        )

        self.MEDIA_LANE_FEC_PM = RegGroupField(consts.MEDIA_LANE_FEC_PM,
            NumberRegField(consts.RX_BITS_PM, self.getaddr(0x34, 128), format=">Q", size=8),
            NumberRegField(consts.RX_BITS_SUB_INTERVAL_PM, self.getaddr(0x34, 136), format=">Q", size=8),
            NumberRegField(consts.RX_CORR_BITS_PM, self.getaddr(0x34, 144), format=">Q", size=8),
            NumberRegField(consts.RX_MIN_CORR_BITS_SUB_INTERVAL_PM, self.getaddr(0x34, 152), format=">Q", size=8),
            NumberRegField(consts.RX_MAX_CORR_BITS_SUB_INTERVAL_PM, self.getaddr(0x34, 160), format=">Q", size=8),
            NumberRegField(consts.RX_FRAMES_PM, self.getaddr(0x34, 168), format=">I", size=4),
            NumberRegField(consts.RX_FRAMES_SUB_INTERVAL_PM, self.getaddr(0x34, 172), format=">I", size=4),
            NumberRegField(consts.RX_FRAMES_UNCORR_ERR_PM, self.getaddr(0x34, 176), format=">I", size=4),
            NumberRegField(consts.RX_MIN_FRAMES_UNCORR_ERR_SUB_INTERVAL_PM, self.getaddr(0x34, 180), format=">I", size=4),
            NumberRegField(consts.RX_MAX_FRAMES_UNCORR_ERR_SUB_INTERVAL_PM, self.getaddr(0x34, 184), format=">I", size=4),
            # TODO: add other PMs...
        )

        # MEDIA_LANE_LINK_PM block corresponds to all the coherent PMs in C-CMIS spec reported in Page 35h.
        self.MEDIA_LANE_LINK_PM = RegGroupField(consts.MEDIA_LANE_LINK_PM,
            NumberRegField(consts.RX_AVG_CD_PM, self.getaddr(0x35, 128), format=">i", size=4),
            NumberRegField(consts.RX_MIN_CD_PM, self.getaddr(0x35, 132), format=">i", size=4),
            NumberRegField(consts.RX_MAX_CD_PM, self.getaddr(0x35, 136), format=">i", size=4),
            NumberRegField(consts.RX_AVG_DGD_PM, self.getaddr(0x35, 140), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_MIN_DGD_PM, self.getaddr(0x35, 142), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_MAX_DGD_PM, self.getaddr(0x35, 144), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_SOPMD_PM, self.getaddr(0x35, 146), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_MIN_SOPMD_PM, self.getaddr(0x35, 148), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_MAX_SOPMD_PM, self.getaddr(0x35, 150), format=">H", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_PDL_PM, self.getaddr(0x35, 152), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MIN_PDL_PM, self.getaddr(0x35, 154), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MAX_PDL_PM, self.getaddr(0x35, 156), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_AVG_OSNR_PM, self.getaddr(0x35, 158), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MIN_OSNR_PM, self.getaddr(0x35, 160), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MAX_OSNR_PM, self.getaddr(0x35, 162), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_AVG_ESNR_PM, self.getaddr(0x35, 164), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MIN_ESNR_PM, self.getaddr(0x35, 166), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MAX_ESNR_PM, self.getaddr(0x35, 168), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_AVG_CFO_PM, self.getaddr(0x35, 170), format=">h", size=2),
            NumberRegField(consts.RX_MIN_CFO_PM, self.getaddr(0x35, 172), format=">h", size=2),
            NumberRegField(consts.RX_MAX_CFO_PM, self.getaddr(0x35, 174), format=">h", size=2),
            NumberRegField(consts.RX_AVG_EVM_PM, self.getaddr(0x35, 176), format=">H", size=2, scale=655.35),
            NumberRegField(consts.RX_MIN_EVM_PM, self.getaddr(0x35, 178), format=">H", size=2, scale=655.35),
            NumberRegField(consts.RX_MAX_EVM_PM, self.getaddr(0x35, 180), format=">H", size=2, scale=655.35),
            NumberRegField(consts.TX_AVG_POWER_PM, self.getaddr(0x35,182), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TX_MIN_POWER_PM, self.getaddr(0x35,184), format=">h", size=2, scale=100.0),
            NumberRegField(consts.TX_MAX_POWER_PM, self.getaddr(0x35,186), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_POWER_PM, self.getaddr(0x35,188), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MIN_POWER_PM, self.getaddr(0x35,190), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MAX_POWER_PM, self.getaddr(0x35,192), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_POWER_PM, self.getaddr(0x35,188), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MIN_POWER_PM, self.getaddr(0x35,190), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MAX_POWER_PM, self.getaddr(0x35,192), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_SIG_POWER_PM, self.getaddr(0x35,194), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MIN_SIG_POWER_PM, self.getaddr(0x35,196), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_MAX_SIG_POWER_PM, self.getaddr(0x35,198), format=">h", size=2, scale=100.0),
            NumberRegField(consts.RX_AVG_SOPROC_PM, self.getaddr(0x35,200), format=">H", size=2),
            NumberRegField(consts.RX_MIN_SOPROC_PM, self.getaddr(0x35,202), format=">H", size=2),
            NumberRegField(consts.RX_MAX_SOPROC_PM, self.getaddr(0x35,204), format=">H", size=2),
            NumberRegField(consts.RX_AVG_MER_PM, self.getaddr(0x35,206), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MIN_MER_PM, self.getaddr(0x35,208), format=">H", size=2, scale=10.0),
            NumberRegField(consts.RX_MAX_MER_PM, self.getaddr(0x35,210), format=">H", size=2, scale=10.0),
            # TODO: add others PMs...
        )
        self.TRANS_CONFIG = RegGroupField(consts.TRANS_CONFIG_FIELD,
            NumberRegField(consts.MODULE_LEVEL_CONTROL, self.getaddr(0x0, 26), size=1, ro=False),
        )

        self.TRANS_CDB = RegGroupField(consts.TRANS_CDB_FIELD,
            NumberRegField(consts.CDB_SUPPORT, self.getaddr(0x01, 163), size=1),
            NumberRegField(consts.CDB_SEQ_WRITE_LENGTH_EXT, self.getaddr(0x01, 164), size=1),
            NumberRegField(consts.CDB_RPL_LENGTH, self.getaddr(0x9f, 134), size=1, ro=False),
            NumberRegField(consts.CDB_RPL_CHKCODE, self.getaddr(0x9f, 135), size=1, ro=False),
        )
        # TODO: add remaining fields

    def getaddr(self, page, offset, page_size=128):
        return page * page_size + offset
