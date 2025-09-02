from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.files.base import File
from django.conf import settings
from pathlib import Path
import os


class Command(BaseCommand):
    help = "Upload all FileField/ImageField media to Cloudinary and update DB references"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not modify database; only report what would be uploaded.",
        )
        parser.add_argument(
            "--delete-local",
            action="store_true",
            help="Delete local files after successful upload.",
        )

    def handle(self, *args, **options):
        dry_run: bool = options["dry_run"]
        delete_local: bool = options["delete_local"]

        media_root = Path(getattr(settings, "MEDIA_ROOT", "media"))
        if not media_root.exists():
            self.stdout.write(self.style.WARNING(f"MEDIA_ROOT not found: {media_root}"))
            return

        updated_count = 0
        skipped_count = 0
        error_count = 0

        for model in apps.get_models():
            file_fields = [f for f in model._meta.get_fields() if getattr(f, "upload_to", None) is not None]
            if not file_fields:
                continue

            qs = model._default_manager.all()
            for instance in qs.iterator():
                for field in file_fields:
                    file_field = getattr(instance, field.name, None)
                    if not file_field:
                        continue

                    name = getattr(file_field, "name", None)
                    if not name:
                        continue

                    # If already a Cloudinary-stored file (url contains res.cloudinary.com), skip
                    try:
                        url = file_field.url
                        if "res.cloudinary.com" in url:
                            skipped_count += 1
                            continue
                    except Exception:
                        pass

                    local_path = media_root / name
                    if not local_path.exists():
                        skipped_count += 1
                        continue

                    self.stdout.write(f"Uploading: {model.__name__}.{field.name} -> {name}")
                    if dry_run:
                        continue

                    try:
                        with open(local_path, "rb") as fp:
                            # Re-save the field using current default storage (Cloudinary)
                            file_field.save(name, File(fp), save=False)
                        instance.save(update_fields=[field.name])
                        updated_count += 1

                        if delete_local:
                            try:
                                os.remove(local_path)
                            except OSError:
                                pass
                    except Exception as exc:
                        error_count += 1
                        self.stderr.write(self.style.ERROR(f"Failed {model.__name__}.{field.name} {name}: {exc}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Updated={updated_count} Skipped={skipped_count} Errors={error_count}"))


