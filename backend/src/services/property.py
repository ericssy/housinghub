import uuid

from sqlalchemy.orm import sessionmaker

from models.property import Property


class PropertyService:

    def __init__(self, logger, database_engine):
        super().__init__()
        Session = sessionmaker(database_engine)
        self.db_session = Session()

    '''
  def add_property(self, property_name: str, address: str, zip_code: str):
    _new_property = Property(id = uuid.uuid4(), property_name = property_name, address = address, zip_code = zip_code)
    self.db_session.add(_new_property)
    self.db_session.commit()
    return _new_property'''

    def add_property(self, property_info):
        _new_property = property_info  # Property(id = uuid.uuid4(), property_name = property_name, address = address,
        # zip_code = zip_code)
        self.db_session.add(_new_property)
        self.db_session.commit()
        return _new_property

    def get_property_by_id(self, pid) -> Property:
        return self.db_session.query(Property).filter(Property.id == pid).one_or_none()

    def get_all_property(self):
        print("get all property")
        return self.db_session.query(Property).all()

    def delete_property(self, pid):
        return self.db_session.query(Property).filter(Property.id == pid).delete(synchronize_session=False)

    def get_properties_by_zip_code(self, zip_code):
        return self.db_session.query(Property).filter(Property.zip_code == zip_code).all()

    def get_properties_by_max_rent(self, max_rent):
        return self.db_session.query(Property).filter(Property.monthly_rent <= max_rent).all()

    def get_properties_by_bedrooms(self, bedrooms):
      return self.db_session.query(Property).filter(Property.bedrooms == bedrooms).all()

    def get_properties_by_housing_type(self, housing_types):
      return self.db_session.query(Property).filter(Property.housing_type.in_(housing_types)).all()

    def get_properties_by_date(self, date):
        return self.db_session.query(Property).filter(Property.date_first_available <= date).all()

    
