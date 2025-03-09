"""Configure."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.mqtt import valid_subscribe_topic

from .const import CONF_PREFIX, DEFAULT_PREFIX, DOMAIN


class OpenAirConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenAir."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            prefix = user_input.get(CONF_PREFIX, DEFAULT_PREFIX)
            if not valid_subscribe_topic(prefix):
                errors["base"] = "invalid_prefix"
            else:
                existing_entries = self._async_current_entries()
                for entry in existing_entries:
                    if entry.data.get(CONF_PREFIX) == prefix:
                        return self.async_abort(reason="already_configured")

                return self.async_create_entry(title="OpenAir", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_PREFIX, default=DEFAULT_PREFIX): str,
                }
            ),
            errors=errors,
        )

    async def async_step_import(self, import_data):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(import_data)
