from abc import ABCMeta, abstractmethod, abstractproperty


__author__ = 'Hans-Werner Roitzsch'

class NetworkCommunicator(metaclass=ABCMeta):
	"""super class for classes, which use any kind of network to communicate with the server"""
	def __init__(self):
		pass
