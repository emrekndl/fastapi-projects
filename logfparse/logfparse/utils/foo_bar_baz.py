from typing import Type

from loguru import logger
from pydantic import BaseModel


def convert_parsed_data_to_schema(
    parsed_data: list, model: Type[BaseModel]
) -> BaseModel:
    fields = list(model.model_fields.keys())
    if len(fields) != len(parsed_data):
        logger.error("Parsed data length does not match model fields.")
        raise ValueError("Parsed data length does not match model fields.")
    return model(**dict(zip(fields, parsed_data)))


# ModelType = TypeVar("ModelType")
# SchemaType = TypeVar("SchemaType", bound=BaseModel)


def convert_to_read_model(model_instance, schema_class):
    return schema_class.model_validate(model_instance)
