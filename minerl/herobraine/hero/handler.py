from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from typing import Dict, Iterator, Any, List, Tuple
import typing
from xml.etree.ElementTree import Element

import gym
import jinja2



class Handler(ABC):
    """Defines the minimal interface for a MineRL handler.

    At their core, handlers should specify unique identifiers
    and a method for producing XML to be given in a mission XML.
    """

    @abstractmethod
    def to_string(self) -> str:
        """The unique identifier for the agent handler.
        This is used for constructing aciton/observation spaces
        and unioning different env specifications.
        """
        raise NotImplementedError()

    # @abstractmethod #TODO: This should be abstract per convention
    # but this strict handler -> xml enforcement will happen
    # with a pyxb update.
    def xml_template(self) -> jinja2.Template:
        """Generates an XML representation of the handler.

        This XML representaiton is templated via Jinja2 and
        has access to all of the member variables of the class.

        Note: This is not an abstract method so that 
        handlers without corresponding XML's can be combined in
        handler groups with group based XML implementations.
        """
        raise NotImplementedError()

    def xml(self) -> str:
        """Gets the XML representation of Handler by templating
        acccording to the xml_template class.


        Returns:
            str: the XML representation of the handler.
        """
        var_dict = {}
        for attr_name in dir(self):
            if 'xml' not in attr_name:
                var_dict[attr_name] = getattr(self, attr_name)
        try:
            return self.xml_template().render(var_dict)
        except jinja2.UndefinedError as e:
            # print the exception with traceback
            message = e.message + "\nOccurred in {}".format(self)
            raise jinja2.UndefinedError(message=message)
            pass

    
    def __or__(self, other):
        """
        Checks to see if self and other have the same to_string
        and if so returns self, otherwise raises an exception.
        """
        assert self.to_string() == other.to_string(), (
            "Incompatible handlers: {self} and {other}".format(**locals()))
        return self


    def __eq__(self, other):
        """
        Checks to see if self and other have the same to_string
        and if so returns self, otherwise raises an exception.
        """
        return self.to_string() == other.to_string()

    def __repr__(self):
        return self.to_string()

