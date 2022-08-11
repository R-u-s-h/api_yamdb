from csv import reader
from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
from django.db.models.fields.related import RelatedField

APP_MODELS = "reviews.models"


class Command(BaseCommand):
    help = "Import data from .csv file to model"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="specify .csv file")
        parser.add_argument(
            "model_name", type=str, help="specify model name to import"
        )

    def _get_model(self, model_name: str, verbosity: int = 1) -> Model:
        try:
            module = import_module(APP_MODELS)
        except ModuleNotFoundError:
            raise CommandError(f"Modue '{APP_MODELS}' not found!")

        if verbosity > 1:
            self.stdout.write(f"Importing module {module}")

        try:
            model = getattr(module, model_name)
        except AttributeError:
            raise CommandError(
                f"Model '{model_name}' not found in module '{module}'!"
            )

        if verbosity > 1:
            self.stdout.write(f"Using model {model}")

        return model

    def handle(self, *args, **options):

        model_name = options.get("model_name")
        model = self._get_model(model_name, options["verbosity"])

        related_fields = {
            field.name
            for field in model._meta.fields
            if isinstance(field, RelatedField)
        }

        with open(options.get("csv_file")) as csv_file:
            field_names: list[str] = list()
            csv_reader = reader(csv_file)

            for field_name in csv_reader.__next__():
                if field_name in related_fields:
                    field_name += "_id"
                field_names.append(field_name)

            for row in csv_reader:
                fields = dict(zip(field_names, row))
                instance, status = model.objects.update_or_create(**fields)
                if options.get("verbosity") > 1:
                    action = "Updated"
                    if status:
                        action = "Created"
                    self.stdout.write(f"{action} instance {instance!r}")
