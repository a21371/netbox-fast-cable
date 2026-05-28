from netbox.plugins import PluginConfig

class FastCableConfig(PluginConfig):
    name = "netbox_fast_cable"
    verbose_name = "Fast Cable"
    description = "Rack-aware click-to-click cable creation"
    version = "0.2.0"
    base_url = "fast-cable"

    def ready(self):
        super().ready()

config = FastCableConfig
