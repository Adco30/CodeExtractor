from abc import ABC

class ConfigurableMixin(ABC):
    # Mixin providing a single apply_config(config: dict) method.
    
    config_map: dict[str, str] = {}

    def apply_config(self, config: dict):
        for key, setter in self.config_map.items():
            if key in config:
                getattr(self, setter)(config[key])
