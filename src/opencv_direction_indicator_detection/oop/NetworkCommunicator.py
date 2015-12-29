__author__ = 'Hans-Werner Roitzsch'

# TODO: is abstract base class, implementation is for example RESTCommunicator

class NetworkCommunicator(metaclass=ABCMeta):
	"""super class for classes, which use any kind of network to communicate with the server"""
	def __init__(self):
		pass
