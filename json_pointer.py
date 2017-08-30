"""
Module:     json_pointer.py
Author:     Chris Ermel
Purpose:    Implements a utility for administering the JSON pointer standard (IETF RFC 6901)
            defined at https://tools.ietf.org/html/rfc6901
"""

from urllib import unquote


#########################
#
# Convenience Functions
#
#########################
def evaluate(pointer, obj):
    """
    Retrieves the attribute specified by param path from param obj.

    --- Example 1 ---

    >>> import json_pointer
    >>> foo = json_pointer.evaluate('/foo', {'foo':'bar'})
    >>> assert foo == 'bar'

    --- Example 2 ---

    >>> foo = json_pointer.evaluate('/foo/-', {'foo': ['bar', 'baz']})
    >>> assert foo == 'baz'

    :param pointer: A string JSON pointer adhering to the IETF RFC 6901 JSON pointer standard for retrieving
        a specific attribute from a JSON-style dictionary.
    :type pointer: str

    :param obj: A dict of key/value pairs.
    :type obj: dict

    :return: The attribute specified by the path attribute, or None if it doesn't exist.
    :rtype: any

    :raises JsonPointerException: When the specified JSON pointer path does not resolve, either because the
        path does not exist within the dict or an out of bounds array index is specified.
    """
    return JsonPointer(pointer).evaluate(obj)


#########################
#
# Classes
#
#########################
class JsonPointer(object):

    #########################
    #
    # String Constants
    #
    #########################
    __SLASH = '/'
    __TILDE = '~'
    __EMPTY_STR = ''
    __ESCAPED_SLASH = '~1'
    __ESCAPED_TILDE = '~0'
    __DASH = '-'
    __ZERO = '0'

    def __init__(self, pointer):
        """
        Creates a new JsonPointer instance based on param pointer.

        :param pointer: The JSON Pointer string used to instantiate the JsonPointer object.
        :type pointer: str
        """
        self.__validate_pointer(pointer)
        self.__pieces = pointer.split(self.__SLASH)[1:]

    def __eq__(self, other):
        """
        Two JsonPointer instances are equal if their string representations are the same.

        :param other: The other JsonPointer instance being compared.
        :type other: JsonPointer

        :return: True if the JsonPointer's are equal, False otherwise.
        :rtype: bool
        """
        # TODO: Potentially override hashing method if necessary
        return str(self) == str(other)

    def __str__(self):
        string = self.__EMPTY_STR
        for piece in self.__pieces:
            string = "{}{}{}".format(string, self.__SLASH, piece)

        return string

    #########################
    #
    # Interface
    #
    #########################
    def evaluate(self, obj):
        """
        Evaluates the JsonPointer against param obj.

        :param obj: A dict of key/value pairs.
        :type obj: dict

        :return: The attribute specified by the path attribute, or None if it doesn't exist.
        :rtype: any

        :raises JsonPointerException: When the specified JSON pointer path does not resolve, either because the
            path does not exist within the dict or an out of bounds array index is specified.
        """
        assert isinstance(obj, dict), 'obj parameter given not a dict'

        # Used for error reporting during array access failures
        last_pointer_piece = None

        for piece in self.__pieces:
            try:
                obj = self.__access_attribute_from_object(piece, obj)
            except (KeyError, TypeError, ValueError):
                raise JsonPointerException('Could not use key "{}" to access JSON given pointer "{}"."'
                                           .format(piece, str(self)))
            except IndexError:
                raise JsonPointerException('Array index "{}" out of bounds for array "{}" given pointer "{}".'
                                           .format(piece, last_pointer_piece, str(self)))
            last_pointer_piece = piece

        return obj

    def move_pointer_forward(self, attribute):
        assert isinstance(attribute, str), 'attribute parameter given not a string.'
        self.__pieces.append(attribute)

    def move_pointer_backward(self):
        self.__pieces.pop()

    #########################
    #
    # Helper Functions
    #
    #########################
    def __access_attribute_from_object(self, key, obj):
        """
        Attempts to access the given key from param obj.

        :param key: The value being used to key into the obj param.
        :type key: str or int

        :param obj: The list or dict object being keyed into by param key.
        :type obj: dict or list

        :return: The object that has been accessed via param key.
        :rtype: dict or list
        """
        if isinstance(obj, dict):
            key = self.__revert_escaped_path_string(
                unquote(key)
            )
        elif isinstance(obj, list):
            if key == self.__DASH:
                # Special case: '-' can be specified to access the final list element
                key = len(obj) - 1
            else:
                if len(key) > 1 and key[0] == self.__ZERO:
                    raise JsonPointerException('Found a leading zero in pointer "{}".'.format(str(self)))
                key = int(key)

        return obj[key]

    def __escape_path_string(self, string):
        """
        Replaces tildes with ~0 and slashes with ~1, if contained within the given string.

        :param string: The path string being escaped.
        :type string: str

        :return: The equivalent path string with slashes and tildes escaped.
        :rtype: str
        """
        return string.replace(self.__TILDE, self.__ESCAPED_TILDE).replace(self.__SLASH, self.__ESCAPED_SLASH)

    def __revert_escaped_path_string(self, string):
        """
        Replaces occurrences of ~0 with tildes and occurrences of ~1 with slashes,
        if contained within the given string.

        :param string: The path string being reverted.
        :type string: str

        :return: The equivalent path string with escaped slashes and tildes reverted.
        :rtype: str
        """
        return string.replace(self.__ESCAPED_SLASH, self.__SLASH).replace(self.__ESCAPED_TILDE, self.__TILDE)

    def __validate_pointer(self, pointer):
        if not isinstance(pointer, str):
            raise JsonPointerException('Pointer parameter "{}" given not a string,'.format(pointer))

        if pointer != self.__EMPTY_STR and pointer[0] != self.__SLASH:
            raise JsonPointerException('Path "{}" given not in correct JSON pointer format.'.format(pointer))


class JsonPointerException(Exception):
    """
    Class for exceptions raised within the json_pointer module.
    """
    pass
