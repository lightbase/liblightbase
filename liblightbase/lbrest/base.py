
from liblightbase.lbrest.core import LBRest

class BaseREST(LBRest):

    """
    """

    def __init__(self, rest_url):
        """
        @param rest_url:
        @param basename:
        """
        super(BaseREST, self).__init__(rest_url)

    def search(self, search_obj='{}'):
        """
        @param search_obj:
        """
        return self.send_request(self.httpget,
            data={self.search_param: search_obj})

    def get(self, base):
        """
        @param name: base's name
        """
        return self.send_request(self.httpget,
            url_path=[base.metadata.name])

    def create(self, base):
        """
        @param base:
        """
        return self.send_request(self.httppost,
            data={self.base_param: base.json})

    def update(self, base):
        """
        @param base:
        """
        return self.send_request(self.httpput,
            url_path=[base.metadata.name],
            data={self.base_param: base.json})

    def delete(self, base):
        """
        @param base:
        """
        return self.send_request(self.httpdelete,
            url_path=[base.metadata.name])
