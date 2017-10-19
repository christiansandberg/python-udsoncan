from udsoncan import Response
from udsoncan.sessions import Session
import inspect
import sys

def cls_from_request_id(given_id):
	return BaseService.from_request_id(given_id)

def cls_from_response_id(given_id):
	return BaseService.from_response_id(given_id)

class BaseService:

	@classmethod	
	def request_id(cls):
		return cls._sid

	@classmethod	
	def response_id(cls):
		return cls._sid + 0x40

	def set_id_from_response_payload(self, payload):
		if not payload or len(payload) == 0:
			raise ValueError("Response is empty")
		_sid = payload[0] - 0x40

	def from_positive_response_payload(self, payload):
		self.set_id_from_response_payload(response)

	@classmethod
	def from_request_id(cls, given_id):
		for name, obj in inspect.getmembers(sys.modules[__name__]):
			if hasattr(obj, "__bases__") and cls in obj.__bases__:
				if obj.request_id() == given_id:
					return obj

	@classmethod
	def from_response_id(cls, given_id):
		for name, obj in inspect.getmembers(sys.modules[__name__]):
			if hasattr(obj, "__bases__") and cls in obj.__bases__:
				if obj.response_id() == given_id:
					return obj

	def subfunction_id(self):
		return 0

	@classmethod
	def use_subfunction(cls):
		if hasattr(cls, '_use_subfunction'):
			return cls._use_subfunction
		else:
			return True
	@classmethod
	def has_custom_positive_response(cls):
		if hasattr(cls, '_custom_positive_response'):
			return cls._custom_positive_response
		else:
			return False

	@classmethod
	def get_name(cls):
		return cls.__name__

def is_valid_service(service_cls):
	return issubclass(service_cls, BaseService)

class DiagnosticSessionControl(BaseService):
	_sid = 0x10
	supported_negative_response = [	Response.Code.SubFunctionNotSupported, 
									Response.Code.IncorrectMessageLegthOrInvalidFormat,
									Response.Code.ConditionsNotCorrect
									]
	def __init__(self, session):
		if isinstance(session, int):
			session = Session.from_id(session)
		
		if not issubclass(session, Session):
			raise ValueError("Given parameter is not a valid Session type")

		self.session = session

	def subfunction_id(self):
		return self.session.get_id()

	def has_subfunction(self):
		return True


class ECUReset(BaseService):
	_sid = 0x01
	def __init__(self):
		pass

# Done
class SecurityAccess(BaseService):
	_sid = 0x27
	class Mode:
		RequestSeed=0
		SendKey=1

	def __init__(self, level, mode=Mode.RequestSeed):
		if mode not in [SecurityAccess.Mode.RequestSeed, SecurityAccess.Mode.SendKey]:
			raise ValueError("Given mode must be either RequestSeed or Send Key ")
		level = int(level)
		if level > 0x7F or level <= 0:
			raise ValueError("Level must be a valid integer between 0 and 0x7F")

		self.level = level
		self.mode = mode

	def subfunction_id(self):
		if self.mode == SecurityAccess.Mode.RequestSeed:
			return (self.level & 0xFE) +1
		elif self.mode == SecurityAccess.Mode.SendKey:
			return (self.level +1) & 0xFE
		else:
			raise ValueError("Cannot generate subfunction ID. Mode is invalid")

class CommunicationControl(BaseService):
	_sid = 0x28
	def __init__(self):
		pass

# Done
class TesterPresent(BaseService):
	_sid = 0x3E


class AccessTimingParameter(BaseService):
	_sid = 0x83
	def __init__(self):
		pass

class SecuredDataTransmission(BaseService):
	_sid = 0x84
	def __init__(self):
		pass

class ControlDTCSetting(BaseService):
	_sid = 0x85
	def __init__(self):
		pass

class ResponseOnEvent(BaseService):
	_sid = 0x86
	def __init__(self):
		pass

class LinkControl(BaseService):
	_sid = 0x87
	def __init__(self):
		pass




def assert_dids_value(dids):
	if not isinstance(dids, int) and not isinstance(dids, list):
		raise ValueError("Data Identifier must either be an integer or a list of integer")

	if isinstance(dids, int):
		if dids < 0 or dids > 0xFFFF:
			raise ValueError("Data Identifier must be set between 0 and 0xFFFF")
	if isinstance(dids, list):
		for did in dids:
			if not isinstance(did, int) or did < 0 or did > 0xFFFF:
				raise ValueError("Data Identifier must be set between 0 and 0xFFFF")

class ReadDataByIdentifier(BaseService):
	_sid = 0x22
	_use_subfunction = False
	_custom_positive_response = True

	def __init__(self, dids):
		assert_dids_value(dids)

		self.dids = dids

class WriteDataByIdentifier(BaseService):
	_sid = 0x2E
	_use_subfunction = False
	_custom_positive_response = True

	def __init__(self, did):
		if not isinstance(did, int):
			raise ValueError('Data Identifier must be an integer value')
		assert_dids_value(did)
		self.did = did



class ReadMemoryByAddress(BaseService):
	_sid = 0x23
	def __init__(self):
		pass

class ReadScalingDataByIdentifier(BaseService):
	_sid = 0x24
	def __init__(self):
		pass

class ReadDataByPeriodicIdentifier(BaseService):
	_sid = 0x2A
	def __init__(self):
		pass

class DynamicallyDefineDataIdentifier(BaseService):
	_sid = 0x2C
	def __init__(self):
		pass



class WriteMemoryByAddress(BaseService):
	_sid = 0x3D
	def __init__(self):
		pass

class ClearDiagnosticInformation(BaseService):
	_sid = 0x14
	def __init__(self):
		pass

class ReadDTCInformation(BaseService):
	_sid = 0x19
	def __init__(self):
		pass

class InputOutputControlByIdentifier(BaseService):
	_sid = 0x2F
	def __init__(self):
		pass

class RoutineControl(BaseService):
	_sid = 0x31
	def __init__(self):
		pass

class RequestDownload(BaseService):
	_sid = 0x34
	def __init__(self):
		pass

class RequestUpload(BaseService):
	_sid = 0x35
	def __init__(self):
		pass

class TransferData(BaseService):
	_sid = 0x36
	def __init__(self):
		pass

class RequestTransferExit(BaseService):
	_sid = 0x37
	def __init__(self):
		pass
