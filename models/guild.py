

class Guild:
    def __init__(
        self,
        id,
        name,
        icon,
        splash,
        discovery_splash,
        owner_id,
        region,
        afk_channel_id,
        afk_timeout,
        verification_level,
        default_message_notifications,
        explicit_content_filter,
        roles,
        emojis,
        features,
        mfa_level,
        system_channel_id,
        system_channel_flags,
        rules_channel_id,
        vanity_url_code,
        description,
        banner,
        premium_tier,
        preferred_locale,
        public_updates_channel_id,
    ):
        self.id = id
        self.name = name
        self.icon = icon
        self.splash = splash
        self.discovery_splash = discovery_splash
        self.owner_id = owner_id
        self.region = region
        self.afk_channel_id = afk_channel_id
        self.afk_timeout = afk_timeout
        self.verification_level = verification_level
        self.default_message_notifications = default_message_notifications
        self.explicit_content_filter = explicit_content_filter
        self.roles = roles
        self.emojis = emojis
        self.features = features
        self.mfa_level = mfa_level
        self.system_channel_id = system_channel_id
        self.system_channel_flags = system_channel_flags
        self.rules_channel_id = rules_channel_id
        self.vanity_url_code = vanity_url_code
        self.description = description
        self.banner = banner
        self.premium_tier = premium_tier
        self.preferred_locale = preferred_locale
        self.public_updates_channel_id = public_updates_channel_id