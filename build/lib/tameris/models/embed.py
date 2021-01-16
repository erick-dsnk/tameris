class EmbedFooter:
    def __init__(self, text = None, icon_url = None, proxy_icon_url = None) -> None:
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedField:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value


class EmbedThumbnail:
    def __init__(self, url, height = None, width = None, proxy_url = None) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width

    
class EmbedImage:
    def __init__(self, url, height = None, width = None, proxy_url = None) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedVideo:
    def __init__(self, url, height = None, width = None) -> None:
        self.url = url
        self.height = height
        self.width = width


class EmbedProvider:
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url


class EmbedAuthor:
    def __init__(self, name, url, icon_url, icon_proxy_url) -> None:
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.icon_proxy_url = icon_proxy_url


class Embed:
    def __init__(
        self,
        title = None,
        description = None,
        url = None,
        timestamp = None,
        color = None,
        footer = None,
        image = None,
        thumbnail = None,
        video = None,
        provider = None,
        author = None,
        fields = []
    ):
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

    @staticmethod
    def create_embed():
        return Embed()

    def set_title(self, title):
        self.title = title
    
    def set_description(self, description):
        self.description = description

    def set_url(self, url):
        self.url = url

    def set_color(self, color):
        self.color = color

    def set_footer(self, text, icon_url = None):
        self.footer = EmbedFooter(
            text=text,
            icon_url=icon_url
        )

    def set_image(self, image_url):
        self.image = EmbedImage(
            url=image_url
        )

    def set_thumbnail(self, thumbnail_url):
        self.thumbnail = EmbedThumbnail(
            url=thumbnail_url
        )

    def set_video(self, video_url):
        self.video = EmbedVideo(
            url=video_url
        )

    def add_field(self, name, value):
        self.fields.append(EmbedField(
            name=name,
            value=value
        ))