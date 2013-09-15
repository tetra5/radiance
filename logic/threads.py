from PyQt4 import QtCore


class ImportingThread(QtCore.QThread):
    """
    Imports modules in a thread. Heaviest imports should be initially here, just
    to be sure that their importing at runtime won't cause UI to hang.
    
    Unfortunately, pyinstaller does not recognize such importing, so the same
    modules should be also fake-imported manually just to be included with
    final distribution.
    
    See radiance.pyinstaller_workaround()
    """
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        
        """
        List of modules to be loaded.
        Each element should contain one of following: 
        
        ('module', ['sub1', 'sub2']) # from module import sub1, sub2
        'module' # import module
        'module.sub1' # import module.sub1
        
        Each module should be also duplicated at radiance.py, for
        pyinstaller to work correctly.
        """
        self.modules = [
#                        'scipy',
                        'scipy.interpolate', 
#                        'matplotlib',
                        'sqlalchemy',
#                        'numpy',
                        ]
        
    def run(self):
        # Actual import.
        for m in self.modules:
            try:
                modname, fromlist = m
            except ValueError:
                modname, fromlist = m, []
                
            try:
                m = __import__(modname, globals(), locals(), fromlist, -1)
            
            except ImportError, e:
                self.emit(QtCore.SIGNAL('terminated'), 
                          'Threaded import: failed to import "%s": %s' % (modname, e))
                
            else:
                self.emit(QtCore.SIGNAL('set_message'), modname)
            
        self.emit(QtCore.SIGNAL('finished()'))
                