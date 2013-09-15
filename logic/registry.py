# -*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod

from settings import settings
from logic.db import NuclideDatabase, MaterialDatabase, \
    LayeredMaterialDatabase, ReportDatabase
from logic import elements
from logic.misc.struct import Struct


#===============================================================================
# Registry
#===============================================================================


class _AbstractRegistry(dict):
    """
    _AbstractRegistry is a dict with special functions, used as an additional
    layer between GUI and database. Registry stores all specified database data
    in memory, which is accessible as class name in global scope. Each element
    consists of {'element_name': object}
    """
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.reload()
    
    @abstractmethod
    def reload(self): 
        pass
    

class NuclideRegistry(_AbstractRegistry):
    
    def reload(self):
        self.clear()
        
        ndb = NuclideDatabase()
        
        for n in ndb.fetch_all():
            try:
                nuclide = elements.get_element(n.title)
            except elements.ElementNotFound:
                raise
            
            kwargs = {
                      'spectre': n.data.get('spectre'),
                      'a_num': nuclide[0],
                      'lat': nuclide[1],
                      'a_mass': n.a_mass,
                      'rus': nuclide[3],
                      'eng': nuclide[2],
                      }
            
            if settings.get('locale') == 'ru_RU':
                self.update({'%s-%d' % (nuclide[3], n.a_mass): Struct(**kwargs)})
                
            else:
                self.update({'%s-%d' % (n.title, n.a_mass): Struct(**kwargs)})
        

class MaterialRegistry(_AbstractRegistry):
        
    def get_by_id(self, material_id):
        for material_title, material in self.iteritems():
            if material.id == material_id:
                return material_title
        
    def reload(self):
        self.clear()
        
        mdb = MaterialDatabase()
        
        for m in mdb.fetch_all():
            
            kwargs = {
                      'id': m.id,
                      'title': m.title,
                      'mu_d': m.data['mu_d'],
                      'b': m.data['b'],
                      'e': m.data['e'],
                      'mass_atten_coeff_x': m.data['mass_attenuation_coefficient'][0],
                      'mass_atten_coeff_y': m.data['mass_attenuation_coefficient'][1],
                      'density': m.data['density'],
                      }
            
            self.update({m.title: Struct(**kwargs)})
            

class LayeredMaterialRegistry(_AbstractRegistry):
    
    def reload(self):
        self.clear()
        
        lmdb = LayeredMaterialDatabase()
        
        try:
            for lm in lmdb.fetch_all():
                kwargs = {
                          'title': lm.title,
                          'layers': lm.data['layers']
                          }
                self.update({lm.title: Struct(**kwargs)})
        except TypeError:
            pass


class ReportRegistry(_AbstractRegistry):
    
    def reload(self):
        self.clear()
        
        rdb = ReportDatabase()
        
        for r in rdb.fetch_all():
            kwargs = {
                      'date': r.date,
                      'data': r.data,
                      'template_type': r.template_type,
                      }
            self.update({r.id: Struct(**kwargs)})
        

# Instantiates registry as a singleton. Use already instantinated variables
# instead of classes when importing

NuclideRegistry = NuclideRegistry()
MaterialRegistry = MaterialRegistry()
LayeredMaterialRegistry = LayeredMaterialRegistry()
ReportRegistry = ReportRegistry()
