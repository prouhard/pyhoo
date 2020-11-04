import abc


class BaseModel(metaclass=abc.ABCMeta):
    def __repr__(self) -> str:
        formatted_attrs = ", ".join(
            attr_name + "=" + attr_value.__repr__() for attr_name, attr_value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({formatted_attrs})"
