# -*- coding: utf-8 -*-
from __future__ import print_function
if __name__ == '__main__':
  raise RuntimeError('\r\n{0}\r\n\r\n  this file is part of retr0chat.\r\n  enter the parent folder of this file and run:\r\n\r\n    python -m r0c <telnetPort> <netcatPort>\r\n\r\n{0}'.format('*'*72))

import gc

# make everything familiar to globals()
from .config  import *
from .util    import *
from .unrag   import *
from .ivt100  import *
from .inetcat import *
from .itelnet import *
from .chat    import *
from .user    import *
from .world   import *

PY2 = (sys.version_info[0] == 2)

if PY2:
  from Queue import Queue
else:
  from queue import Queue



def memory_dump():
	import gc
	import _pickle as cPickle
	with open("profiler-results.memory", 'wb') as dump:
		for obj in gc.get_objects():
			i = id(obj)
			size = sys.getsizeof(obj, 0)
			#    referrers = [id(o) for o in gc.get_referrers(obj) if hasattr(o, '__class__')]
			referents = [id(o) for o in gc.get_referents(obj) if hasattr(o, '__class__')]
			if hasattr(obj, '__class__'):
				cls = str(obj.__class__)
				cPickle.dump({'id': i, 'class': cls, 'size': size, 'referents': referents}, dump)



def get_obj_name(target_id):
	variables = {**locals(), **globals()}
	for var in variables:
		exec('var_id=id({0})'.format(var))
		if var_id == target_id:
			exec('found={0}'.format(var))
	if found:
		print(found)
		print(id(found))
	else:
		print('/')

def find_leaked_messages():
	n_hits = 0
	for obj in gc.get_objects():
		if not type(obj) is Message:
			continue
		n_hits += 1
		if n_hits > 1000:
			break
		
		ref_objs = gc.get_referents(obj)
		referents = [id(o) for o in ref_objs if hasattr(o, '__class__')]
		print('obj,ref:',id(obj),referents)
		print('obj:',obj)
		print('ref:',ref_objs)
		print()

repl_notepad = """

from .diag import *
find_leaked_messages()

n_hits = 0
for obj in gc.get_objects():
  if not hasattr(obj, '__class__'):
    continue
  if type(obj) is Message:
    n_hits += 1
    if n_hits > 10000:
      break
    i = id(obj)
    size = sys.getsizeof(obj, 0)
    name = obj.__name__ if hasattr(obj, '__name__') else '/'
    referents = [id(o) for o in gc.get_referents(obj) if hasattr(o, '__class__')]
    print('id: {0}, size: {1}, class: {2}, name: {3}, referents: {4}'.format(
      i, size, str(obj.__class__), name, ', '.join([str(x) for x in referents])))

"""