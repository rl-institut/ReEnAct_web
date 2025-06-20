from django.apps import AppConfig


class ReenactConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reenact.reenact"

    def ready(self) -> None:
        """Content in here is run when app is ready."""
        # pylint: disable=C0415
        from django_oemof import hooks

        # pylint: disable=C0415
        from reenact.reenact import hooks as reenact_hooks

        hooks.register_hook(
            hooks.HookType.SETUP,
            hooks.Hook(
                scenario=hooks.ALL_SCENARIOS,
                function=reenact_hooks.set_up_volatiles,
            ),
        )

        hooks.register_hook(
            hooks.HookType.MODEL,
            hooks.Hook(
                scenario=hooks.ALL_SCENARIOS,
                function=reenact_hooks.track_emissions,
            ),
        )

        hooks.register_hook(
            hooks.HookType.POSTPROCESSING,
            hooks.Hook(
                scenario=hooks.ALL_SCENARIOS,
                function=reenact_hooks.store_emission,
            ),
        )
