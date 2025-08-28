from django.apps import AppConfig


class PropertycrudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'propertyCrud'

    def ready(self):  # noqa: D401
        # Connect a signal to print when DB connects
        from django.db.backends.signals import connection_created

        def on_connection_created(sender, connection, **kwargs):
            try:
                vendor = getattr(connection, 'vendor', 'unknown')
                settings_name = getattr(connection, 'settings_dict', {}).get('NAME', 'unknown')
                print(f"[DB CONNECTED] vendor={vendor} db={settings_name}")
            except Exception:  # pragma: no cover
                print("[DB CONNECTED]")

        connection_created.connect(on_connection_created)