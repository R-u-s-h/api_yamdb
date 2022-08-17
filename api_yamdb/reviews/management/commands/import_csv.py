from csv import reader
from importlib import import_module
from typing import Optional

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

    def get_model(
        self,
        module_name: str,
        model_name: str,
        verbosity: int = 1,
    ) -> Model:
        """Imports the specified model from the specified module.

        Args:
            module_name (str): module name to import model from
            model_name (str): model name to import
            verbosity: log level according manage.py rules

        Returns:
           Model: imported model
        """
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            raise CommandError(f"Modue '{module_name}' not found!")

        if verbosity > 1:
            self.stdout.write(f"Importing module '{module}'")

        try:
            model = getattr(module, model_name)
        except AttributeError:
            raise CommandError(
                f"Model '{model_name}' not found in module '{module}'!"
            )

        if verbosity > 1:
            self.stdout.write(f"Using model {model}")

        return model

    @staticmethod
    def get_related_fields(model: Model) -> set[Optional[str]]:
        """Returns a set of relational fields from Model.

        Args:
            model (Model): Django model

        Returns:
             set[Optional[str]]: set of field names which are subclass of
                RelatedField or empty set if no relations are in model
        """
        return {
            field.name
            for field in model._meta.fields
            if isinstance(field, RelatedField)
        }

    def update_or_create(
        self, model: Model, fields: dict[str, str], verbosity: int = 1
    ) -> None:
        """Updates model or creates if model with specified id doesn't exist"""

        try:
            instance = model.objects.get(id=fields.get("id"))
            for field, value in fields.items():
                setattr(instance, field, value)
            action = "updated"

        except model.DoesNotExist:
            instance = model(**fields)
            action = "created"

        try:
            instance.save()
        except Exception as e:
            if verbosity > 0:
                self.stdout.write(
                    self.style.ERROR(
                        f"Can't create or update model instance: {e}"
                    )
                )
        else:
            if verbosity > 1:
                self.stdout.write(f"'{instance!r}' has been {action}.")

    def handle(self, *args, **options):

        model = self.get_model(
            module_name=APP_MODELS,
            model_name=options["model_name"],
            verbosity=options["verbosity"],
        )

        related_fields = self.get_related_fields(model)

        with open(options.get("csv_file")) as csv_file:
            csv_reader = reader(csv_file)

            # Получаем имена полей из первой строчки csv-файла
            field_names: list[str] = list()
            first_row = csv_reader.__next__()
            for field_name in first_row:
                if field_name in related_fields:
                    field_name += "_id"
                field_names.append(field_name)

            for row in csv_reader:
                fields = dict(zip(field_names, row))
                self.update_or_create(
                    model=model,
                    fields=fields,
                    verbosity=options["verbosity"],
                )
