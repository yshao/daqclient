__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '1:57 PM'

def _pickle_method(method):
	func_name = method.im_func.__name__
	obj = method.im_self
	cls = method.im_class
	if func_name.startswith('__') and not func_name.endswith('__'): #deal with mangled names
		cls_name = cls.__name__.lstrip('_')
		func_name = '_' + cls_name + func_name
	return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
	for cls in cls.__mro__:
		try:
			func = cls.__dict__[func_name]
		except KeyError:
			pass
		else:
			break
	return func.__get__(obj, cls)

import copy_reg
import types

def mp_reg():
    copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)