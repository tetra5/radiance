# -*- coding: utf-8 -*-


"""
Created on 13.10.2010

@author: vda
"""


from sqlalchemy import Column, Integer, String, PickleType, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic import elements


Base = declarative_base()
ReportBase = declarative_base()


class _Report(ReportBase):
    __tablename__ = '_reports'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    data = Column(PickleType)
    template_type = Column(Integer)
    
    def __init__(self, date, data, template_type):
        """
        @param date: report date, pythonic datetime
        @param data: dict of template variables for jinja2 template engine
        @param template_type: template type, see settings.TEMPLATE_TYPES
        """
        
        self.date = date
        self.data = data
        self.template_type = template_type


class _Nuclide(Base):
    __tablename__ = '_nuclides'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    a_mass = Column(Integer)
    data = Column(PickleType)
    
    def __init__(self, title, a_mass, data):
        """
        @param name: nuclide name
        @param a_mass: atomic mass
        @param data: nuclide parameters, see below.
        """
        # data = {
        #         'spectre': list of floats,
        #         }
        
        self.title = title
        self.a_mass = a_mass
        self.data = data


class ReportDatabase(object):
    def __init__(self, db_path=None, debug=False):
        if not db_path:
            db_path = 'reports.db'
            
        try:
            engine = create_engine('sqlite:///%s' % db_path, echo=debug)
        except:
            raise
        
        ReportBase.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
        
    def add(self, date, data, template_type):
        report = _Report(date, data, template_type)
        self.session.add(report)
        self.session.commit()
    
    def fetch_by_id(self, report_id):
        return self.session.query(_Report).filter_by(id=report_id).first()
    
    def fetch_all(self):
        return self.session.query(_Report).all()


class NuclideDatabase(object):
    def __init__(self, db_path=None, debug=False):
        if not db_path:
            db_path = 'radiance.db'
        
        try:
            engine = create_engine('sqlite:///%s' % db_path, echo=debug)
        except:
            raise
        
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
    
    def _find_nuclide(self, nuclide):
        try: 
            title, a_mass = nuclide.split('-')
        except ValueError:
            raise
        
        try:
            element = elements.get_element(title)
        except elements.ElementNotFound:
            raise
        
        #returns english element name and its atomic_mass
        return element[2], a_mass
    
    def fetch(self, nuclide):
        try:
            eng, a_mass = self._find_nuclide(nuclide)
        except:
            raise
        
        return self.session.query(_Nuclide).filter_by(title=eng, a_mass=a_mass).first()
    
    def fetch_all(self):
        return self.session.query(_Nuclide).all()
    
    def add(self, title, a_mass, data):
        nuclide = _Nuclide(unicode(title), a_mass, data)
        self.session.add(nuclide)
        self.session.commit()
    
    def remove(self, nuclide):
        try:
            eng, a_mass = self._find_nuclide(nuclide)
        except:
            raise
        
        self.session.query(_Nuclide).filter_by(title=eng, a_mass=a_mass).delete()
        self.session.commit()
    
    def update(self, nuclide, **kwargs):
        try:
            eng, a_mass = self._find_nuclide(nuclide)
        except:
            raise
        
        self.session.query(_Nuclide).filter_by(title=eng, a_mass=a_mass).update(kwargs)
        self.session.commit()


class _Material(Base):
    __tablename__ = '_materials'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    data = Column(PickleType)
    
    def __init__(self, title, data):
        """
        @param title: material name
        @param data: material parameters, see below
        """
        # data = {
        #         'mu_d': list of floats,
        #         'e': list of floats,
        #         'b': list of lists of floats,
        #         'mass_attenuation_coefficient': list of 2 lists of floats,
        #             1st list is X
        #             2nd list is F(X)
        #         'density': float,
        #         }
        
        self.title = title
        self.data = data
        

class _LayeredMaterial(Base):
    __tablename__ = '_layered_materials'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    data = Column(PickleType)
    
    def __init__(self, title, data):
        """
        @param title: layered material name
        @param data: layered material parameters, see below
        """
        # data = {
        #         'layers': [
        #                    [material_id1 (int), thickness1 (float),
        #                    [material_id2 (int), thickness2 (float), ...
        #                    ]
        #        }   
        
        self.title = title
        self.data = data
        

class LayeredMaterialDatabase(object):
    def __init__(self, db_path=None, debug=False):
        if not db_path:
            db_path = 'radiance.db'
        
        try:
            engine = create_engine('sqlite:///%s' % db_path, echo=debug)
        except:
            raise Exception
        
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
        
    def fetch(self, layered_material):
        return self.session.query(_LayeredMaterial).filter_by(title=layered_material).first()
    
    def fetch_all(self):
        return self.session.query(_LayeredMaterial).all()
    
    def add(self, title, data):
        layered_material = _LayeredMaterial(unicode(title), data)
        self.session.add(layered_material)     
        self.session.commit()
        
    def remove(self, layered_material):
        self.session.query(_LayeredMaterial).filter_by(title=layered_material).delete()
        self.session.commit()
        
    def update(self, layered_material, **kwargs):
        self.session.query(_LayeredMaterial).filter_by(title=layered_material).update(kwargs)
        self.session.commit()


class MaterialDatabase(object):
    def __init__(self, db_path=None, debug=False):
        if not db_path:
            db_path = 'radiance.db'
        
        try:
            engine = create_engine('sqlite:///%s' % db_path, echo=debug)
        except:
            raise Exception
        
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
        
    def fetch(self, material):
        return self.session.query(_Material).filter_by(title=material).first()
    
    def fetch_by_id(self, material_id):
        return self.session.query(_Material).filter_by(id=material_id).first()
    
    def fetch_all(self):
        return self.session.query(_Material).all()
    
    def add(self, title, data):
        material = _Material(title, data)
        self.session.add(material)
        self.session.commit()
        
    def remove(self, material):
        self.session.query(_Material).filter_by(title=material).delete()
        self.session.commit()
        
    def update(self, material, **kwargs):
        self.session.query(_Material).filter_by(title=material).update(kwargs)
        self.session.commit()


if __name__ == '__main__':
    pass

    ldb = LayeredMaterialDatabase('../radiance.db', debug=True)
    title = 'Layered material test'
    data = {
            'layers': [
                       [1, 1.0],
                       [2, 2.0],
                       ],
            }
    ldb.add(title, data)
    print ldb.fetch_all()
    
#    ndb = NuclideDatabase('../radiance.db', debug=True)
#    data = {
#            'spectre': [
#                        [1.060, 0.0040],
#                        [0.613, 0.0634],
#                        [0.604, 0.1090],
#                        [0.588, 0.0565],
#                        [0.485, 0.0293],
#                        [0.468, 0.4750],
#                        [0.417, 0.0127],
#                        [0.375, 0.0146],
#                        [0.316, 0.8330],
#                        [0.308, 0.2720],
#                        [0.296, 0.2610],
#                        [0.283, 0.0049],
#                        [0.206, 0.0273],
#                        [0.201, 0.0034],
#                        ],
#            }
#    ndb.add('Iridium', 192, data)
#    print ndb.fetch_all()
#    
#    mdb = MaterialDatabase('../radiance.db', debug=True)
#    data = {
#            'mu_d': [1, 2, 4, 7, 10, 15, 20],
#            'e': [0.15, 0.3, 0.4, 0.5, 1.0, 2.0, 3.0, 4.0, 5.1, 6.0, 8.0, 10.0],
#            'b': [
#                  [1.01, 1.03, 1.06, 1.15, 1.16, 1.18, 1.19],
#                  [1.11, 1.17, 1.25, 1.34, 1.41, 1.50, 1.56],
#                  [1.17, 1.29, 1.46, 1.58, 1.72, 1.89, 2.02],
#                  [1.24, 1.42, 1.69, 2.00, 2.27, 2.65, 2.73],
#                  [1.37, 1.69, 2.26, 3.02, 3.74, 4.81, 5.86],
#                  [1.39, 1.76, 2.51, 3.66, 4.84, 6.87, 9.00],
#                  [1.34, 1.68, 2.43, 3.75, 5.30, 8.44, 12.3],
#                  [1.27, 1.56, 2.25, 3.61, 5.44, 9.80, 16.3],
#                  [1.21, 1.46, 2.08, 3.44, 5.55, 11.7, 23.6],
#                  [1.18, 1.40, 1.97, 3.34, 5.69, 13.8, 32.7],
#                  [1.14, 1.30, 1.74, 2.89, 5.07, 14.1, 44.6],
#                  [1.11, 1.23, 1.58, 2.52, 4.34, 12.5, 39.2]
#                  ],
#            'mass_attenuation_coefficient': [
#                [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0], # x
#                [5.32, 1.9, 0.933, 0.369, 0.215, 0.15, 0.117, 0.084, 0.068, 0.0508, 0.0451, 0.0416, 0.0416, 0.0424, 0.0433, 0.0456, 0.0488] # f(x)
#                ],
#            'density': 11.3,
#            }
#    
#    mdb.add(u'Свинец', data)
#    print mdb.fetch_all()

