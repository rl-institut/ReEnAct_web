"""Oemof simulation hooks are registered when application is ready."""

from django.apps import AppConfig


class ReenactConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reenact.reenact"

    def ready(self) -> None:
        """Register hooks."""
        # pylint: disable=C0415
        from django_oemof import hooks

        # pylint: disable=C0415
        from reenact.reenact import hooks as reenact_hooks

        hooks.register_hook(
            hooks.HookType.SETUP,
            hooks.Hook(
                scenario=hooks.ALL_SCENARIOS,
                function=reenact_hooks.set_up_oemof_components_from_user_input,
            ),
        )
