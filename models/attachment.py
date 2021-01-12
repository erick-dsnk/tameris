

class Attachment:
    def __init__(
        self,
        id,
        filename,
        size,
        url,
        proxy_url,
        **kwargs
    ):
        self.id = id
        self.filename = filename
        self.size = size
        self.url = url
        self.proxy_url = proxy_url

        if 'height' in kwargs.keys() and 'width' in kwargs.keys():
            self.height = kwargs['height']
            self.width = kwargs['width']