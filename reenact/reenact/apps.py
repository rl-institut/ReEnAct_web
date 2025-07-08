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
                function=reenact_hooks.set_up_oemof_components_from_user_input,
            ),
        )

        hooks.register_hook(
            hook_type=hooks.HookType.MODEL,
            hook=hooks.Hook(hooks.ALL_SCENARIOS, reenact_hooks.model_co2_tracking),
        )
        hooks.register_hook(
            hook_type=hooks.HookType.MODEL,
            hook=hooks.Hook(hooks.ALL_SCENARIOS, reenact_hooks.model_co2_limit),
        )
        hooks.register_hook(
            hook_type=hooks.HookType.MODEL,
            hook=hooks.Hook(hooks.ALL_SCENARIOS, reenact_hooks.model_co2_cost),
        )
        hooks.register_hook(
            hook_type=hooks.HookType.MODEL,
            hook=hooks.Hook(hooks.ALL_SCENARIOS, reenact_hooks.model_prod_goal),
        )

        hooks.register_hook(
            hooks.HookType.POSTPROCESSING,
            hooks.Hook(
                scenario=hooks.ALL_SCENARIOS,
                function=reenact_hooks.store_emission,
            ),
        )
