class EmbedFooter:
    def __init__(self, text, icon_url, proxy_icon_url) -> None:
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedField:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value


class EmbedThumbnail:
    def __init__(self, url, proxy_url, height, width) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width

    
class EmbedImage:
    def __init__(self, url, proxy_url, height, width) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedVideo:
    def __init__(self, url, height, width) -> None:
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
        title,
        description,
        url,
        timestamp,
        color,
        footer,
        image,
        thumbnail,
        video,
        provider,
        author,
        fields
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