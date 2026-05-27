from sonic_platform_base.sonic_xcvr.api.public.cmis import CmisApi


NvidiaSpc6OeId = 0x0001
NvidiaSpc6ElspId = 0x0002

class NvidiaOeMemMap(CmisMemMap):
    def __init__(self, codes):
        super().__init__(codes)

class NvidiaElspMemMap(ElspMemMap):
    def __init__(self, codes):
        super().__init__(codes)

class CpoBase(object): #Similar to Sfp object but for CPO consists of OE and ELSP objects
     def __init__(self, oe_bank_id=0, elsfp_bank_id=0, hardware_id: CpoHardwareId):
        self.oe_bank_id = oe_bank_id
        self.elsfp_bank_id = elsfp_bank_id
        self.oe = OeBase(oe_bank_id, hardware_id)
        self.elsfp = ElspBase(elsfp_bank_id, hardware_id)
        pass  
     
     def do_fiber_check(self, lane):
         oe_api = self.oe.get_oe_api()
         oe_api.do_fiber_check(lane)   
         pass
     
     def tx_disable(self, lane):
         elsp_api = self.elsfp.get_elsp_api()
         elsp_api.tx_disable(lane)
         pass
 
class CpoOptoeBase():
    """Provides Optoe driver functionality for OE/ELSP I2C devices"""
    def set_optoe_write_max(self, sys_path, write_max):
        pass

    def get_oe_eeprom_path(self):
        NotImplemented

    def write_oe_eeprom(self, offset, num_bytes, write_buffer):
        # get_oe_eeprom_path()
        # write to the sysfs
        pass

    def read_oe_eeprom(self, offset, num_bytes):
        # get_oe_eeprom_path()
        # read from the sysfs
        pass

    def write_elsp_eeprom(self, offset, num_bytes, write_buffer):
        # get_oe_eeprom_path()
        # write to the sysfs
        pass

    def read_elsp_eeprom(self, offset, num_bytes):
        # get_oe_eeprom_path()
        # read from the sysfs
        pass

class CpoOeApiFactory():
    def __init__(self, oe):
        self._oe = oe

    def _create_api(self, codes_class, mem_map_class, api_class):
        mem_map = mem_map_class(codes_class, self._oe.bank_id)
        oe_eeprom = XcvrEeprom(self.oe.read_eeprom, self.oe.write_eeprom, mem_map)
        return api_class(oe_eeprom)

    def create_oe_api(self, hardware_id: CpoHardwareId, bank=0):
        if hardware_id.oe_id == NvidiaSpc6OeId:
            return self._create_api(
                codes_class=NvidiaCmisCodes,
                mem_map_class=NvidiaCmisMemMap,
                api_class=CmisApi,
                #reader=self.oe_eeprom.reader,
                #writer=self.oe_eeprom.writer,
                bank=bank
            )

        raise ValueError(f"Could not determine what OE API to use for OE ID: {hardware_id.oe_id}")
    

class CpoElspApiFactory():
    def __init__(self, elsp):
        self._elsp = elsp

    def _create_api(self, codes_class, mem_map_class, api_class):
        mem_map = mem_map_class(codes_class, self._elsp.bank_id)
        oe_eeprom = XcvrEeprom(self.elsp.read_eeprom, self._elsp.write_eeprom, mem_map)
        return api_class(oe_eeprom)

    def create_elsp_api(self, hardware_id: CpoHardwareId, bank=0):
        if hardware_id.elsp_id is None:
            # read eeprom vendor and identifier
            # create Vendor specific Elsp API
            return VendorSpecificElspApi()
        
        elif hardware_id.elsp_id == NvidiaElspId:
            return self._create_api(
                codes_class=NvidiaElspCodes,
                mem_map_class=NvidiaElspMemMap,
                api_class=NvidiaElspApi,
                #reader=self.elsp_eeprom.reader,
                #writer=self.elsp_eeprom.writer,
                bank=bank
            )

class OeBase(CpoOptoeBase):
     def __init__(self, bank_id=0, hardware_id: CpoHardwareId):
         self.bank_id = bank_id
         self._oe_api = None
         self.hardware_id = hardware_id

     def read_eeprom(self):
         super().read_oe_eeprom()
         pass
     
     def write_eeprom(self):
         super().write_oe_eeprom()
     
     def do_fiber_check(lane):
         pass
     
     def refresh_oe_api(self):
        self._oe_api = self._oe_api_factory.create_oe_api(self)

     def get_oe_api(self):
        if self._oe_api is None:
            self.refresh_oe_api()
        return self._oe_api 

class ElspBase(CpoOptoeBase):
     def __init__(self, bank_id=0, hardware_id: CpoHardwareId = None):
         self.bank_id = bank_id
         self._elsp_api = None
         self.hardware_id = hardware_id

     def read_eeprom(self):
         super().read_elsp_eeprom()
         pass

     def write_eeprom(self):
         super().write_elsp_eeprom()
         pass

     def tx_disable(self):
         pass
     
     def refresh_elsp_api(self):
        self._elsp_api = self._elsp_api_factory.create_elsp_api(self)

     def get_elsp_api(self):
        if self._elsp_api is None:
            self.refresh_elsp_api()
        return self._elsp_api 

