
from datetime import datetime
from liblightbase.lbutils.const import PYSTR

class DocumentMetadata(object):

    """ 
    The document metadata is all data related to the document. The main purpose
    of metadata is to facilitate in the discovery of relevant information, more 
    often classified as resource discovery.
    """

    def __init__(self, id_doc, dt_doc, dt_last_up, dt_idx=None,
            dt_del=None):

        """ Class constructor. Sets document metadata attributes. 
        """

        # @property id_doc: The primary key for document's table 
        # and uniquely identify each document in the table.
        self.id_doc = id_doc

        # @property dt_doc: The document's creation date 
        # (date and time).
        self.dt_doc = dt_doc

        # @property dt_last_up: The document's last updating date 
        # (date and time).
        self.dt_last_up = dt_last_up

        # @property dt_idx: The document's date (date and time) of indexing. 
        # All routines that index the document must fill this field.
        self.dt_idx = dt_idx

        # @property dt_del: The document's date (date and time) of deletion. 
        # This date is filled when he normal deletion process failed when 
        # deleting the document index. When it happens, the document is cleared 
        # up, leaving only it's metadata.
        self.dt_del = dt_del

    @property
    def __dict__(self):
        """ Dictionary format of document metadata model.
        """
        return {
           'id_doc' : self.id_doc,
           'dt_doc' : self.dt_doc,
           'dt_last_up' : self.dt_last_up,
           'dt_idx' : self.dt_idx,
           #'dt_del' : self.dt_del
        }

    def _attr_setter(self, attr, value, accepted_types):
        """
        Class custom setter. Verify if value is instance of one of 
        accepted_types and set private attribute to class.
        @param attr: attribute name.
        @param value: attribute value to be setted.
        @param accepted_types: tuple of types.
        """
        try:
            assert(isinstance(value, accepted_types))
        except AssertionError:
            raise TypeError('{0} must be of type {1}'.format(
                attr, accepted_types))
        else:
            setattr(self, '_' + attr, value)

    @property
    def id_doc(self):
        """ @property id_doc getter
        """
        return self._id_doc

    @id_doc.setter
    def id_doc(self, value):
        """ @property id_doc setter
        """
        accepted_types = (int,)
        self._attr_setter('id_doc', value, accepted_types)

    @property
    def dt_doc(self):
        """ @property dt_doc getter
        """
        return self._dt_doc

    @dt_doc.setter
    def dt_doc(self, value):
        """ @property dt_doc setter
        """
        if isinstance(value, PYSTR):
            value = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        accepted_types = (datetime,)
        self._attr_setter('dt_doc', value, accepted_types)

    @property
    def dt_last_up(self):
        """ @property dt_last_up getter
        """
        return self._dt_last_up

    @dt_last_up.setter
    def dt_last_up(self, value):
        """ @property dt_last_up setter
        """
        if isinstance(value, PYSTR):
            value = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        accepted_types = (datetime,)
        self._attr_setter('dt_last_up', value, accepted_types)

    @property
    def dt_idx(self):
        """ @property dt_idx getter
        """
        return self._dt_idx

    @dt_idx.setter
    def dt_idx(self, value):
        """ @property dt_idx setter
        """
        if isinstance(value, PYSTR):
            value = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        accepted_types = (datetime, type(None))
        self._attr_setter('dt_idx', value, accepted_types)

    @property
    def dt_del(self):
        """ @property dt_del getter
        """
        return self._dt_del

    @dt_del.setter
    def dt_del(self, value):
        """ @property dt_del setter
        """
        if isinstance(value, PYSTR):
            value = datetime.strptime(value, '%d/%m/%Y %H:%M:%S')
        accepted_types = (datetime, type(None))
        self._attr_setter('dt_del', value, accepted_types)
