import copy
import warnings
from collections import defaultdict

__all__ = [
    "get_all_keys",
    "get_occurrences_and_values",
    "get_occurrence_of_value",
    "get_occurrence_of_key",
    "nested_update",
    "nested_delete",
    "nested_alter",
    "nested_lookup",
]


# TODO: get rid of this global values_list
values_list = []


def nested_lookup(key, document, wild=False, with_keys=False):
    """Lookup a key in a nested document, return a list of values"""
    if with_keys:
        d = defaultdict(list)
        for k, v in _nested_lookup(key, document, wild=wild, with_keys=with_keys):
            d[k].append(v)
        return d
    return list(_nested_lookup(key, document, wild=wild, with_keys=with_keys))


def _is_case_insensitive_substring(a, b):
    """return True if `a` is a case insensitive substring of `b`, else False"""
    return str(a).lower() in str(b).lower()


def _nested_lookup(key, document, wild=False, with_keys=False):
    """Lookup a key in a nested document, yield a value"""
    if isinstance(document, list):
        for d in document:
            for result in _nested_lookup(key, d, wild=wild, with_keys=with_keys):
                yield result

    if isinstance(document, dict):
        for k, v in document.items():
            if key == k or (wild and _is_case_insensitive_substring(key, k)):
                if with_keys:
                    yield k, v
                else:
                    yield v
            if isinstance(v, dict):
                for result in _nested_lookup(key, v, wild=wild, with_keys=with_keys):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in _nested_lookup(
                        key, d, wild=wild, with_keys=with_keys
                    ):
                        yield result


def get_all_keys(dictionary):
    """
    Method to get all keys from a nested dictionary as a List
    Args:
        dictionary: Nested dictionary
    Returns:
        List of keys in the dictionary
    """
    result_list = []

    def recrusion(document):
        if isinstance(document, list):
            for list_items in document:
                recrusion(document=list_items)
        elif isinstance(document, dict):
            for key, value in document.items():
                result_list.append(key)
                recrusion(document=value)
        return

    recrusion(document=dictionary)
    return result_list


def get_occurrence_of_key(dictionary, key):
    """
    Method to get occurrence of a key in a nested dictionary

    Args:
        dictionary: Nested dictionary
        key: Key to search for the occurrences
    Return:
        Number of occurrence (Integer)
    """
    return _get_occurrence(dictionary=dictionary, item="key", keyword=key)


def get_occurrences_and_values(items, value):
    """
    Method to get occurrence of a value in a nested list of dictionary

    Args:
        items: list of dictionary: Nested dictionary
        value: Value to search for the occurrences

    Return:
        Dict where the key is the value arg and his value is a new
        dict with occurrences and values
    """
    occurrences = {}
    occurrence = 0
    value_list = []

    for item in items:
        occurrence_result, values = _get_occurrence_with_values(
            dictionary=item, item="value", keyword=value
        )
        occurrence = occurrence + occurrence_result
        if occurrence_result:
            value_list.extend(values)

    occurrences[value] = {"occurrences": occurrence, "values": value_list}

    return occurrences


def _get_occurrence_with_values(dictionary, item, keyword):
    occurrence = [0]

    result_recursion = _recursion(dictionary, item, keyword, occurrence, True)

    global values_list
    values_list = []

    return occurrence[0], result_recursion


def get_occurrence_of_value(dictionary, value):
    """
    Method to get occurrence of a value in a nested dictionary

    Args:
        dictionary: Nested dictionary
        value: Value to search for the occurrences
    Return:
        Number of occurrence (Integer)
    """
    return _get_occurrence(dictionary=dictionary, item="value", keyword=value)


def _recursion(dictionary, item, keyword, occurrence, with_values=False):
    global values_list

    if item == "key":
        if dictionary.get(keyword) is not None:
            occurrence[0] += 1
    elif keyword in list(dictionary.values()):
        occurrence[0] += list(dictionary.values()).count(keyword)
        if with_values:
            values_list.append(dictionary)
    for key, value in dictionary.items():
        if isinstance(value, dict):
            _recursion(value, item, keyword, occurrence, with_values)
        elif isinstance(value, list):
            for list_items in value:
                if hasattr(list_items, "items"):
                    _recursion(list_items, item, keyword, occurrence, with_values)
                elif list_items == keyword:
                    occurrence[0] += 1 if item == "value" else 0

    if values_list:
        return values_list


def _get_occurrence(dictionary, item, keyword):
    """
    Method to get occurrence of a key or value in a nested dictionary

    Args:
        dictionary: Nested dictionary
        item: Mostly (key or value)
        keyword: key word to find occurrence
    Return:
        Number of occurrence of the given keyword in the dict
    """
    occurrence = [0]
    _recursion(dictionary, item, keyword, occurrence)

    global values_list
    values_list = []

    return occurrence[0]


def nested_delete(document, key, in_place=False):
    if not in_place:
        document = copy.deepcopy(document)
    return _nested_delete(document=document, key=key)


def _nested_delete(document, key):
    """
    Method to delete a key->value pair from a nested document
    Args:
        document: Might be List of Dicts (or) Dict of Lists (or)
         Dict of List of Dicts etc...
        key: Key to delete
    Return:
        Returns a document that includes everything but the given key
    """
    if isinstance(document, list):
        for list_items in document:
            _nested_delete(document=list_items, key=key)
    elif isinstance(document, dict):
        if document.get(key):
            del document[key]
        for dict_key, dict_value in document.items():
            _nested_delete(document=dict_value, key=key)
    return document


def nested_update(document, key, value, in_place=False, treat_as_element=True):
    """
    Method to update a key->value pair in a nested document

    Args:
        document: Might be List of Dicts (or) Dict of Lists (or)
            Dict of List of Dicts etc...

        key: Key to update the value

        value: Value to set

        in_place (bool):
            True: modify the dict in place;
            False: create a deep copy of the dict and modify it
            Defaults to False

        treat_as_element (bool):
            True: if a list is provided as "value", the function trys
                to match the list elements to the occurences of the key.
                If the key occures more often than the provided list has
                elements, the first element gets recycled.
            False: the provided list is treated as one scalar value and
                will be set as value to every key that matches.
            Defaults to True (because of backwards portability of the package).

    Return:
        Returns a document that has updated key, value pair.
    """

    # check if a list or scalar value is provided and create a list
    # from the scalar value
    # check the length of the list and provide it to _nested_update
    if not treat_as_element and not isinstance(value, list):
        raise Exception("The value must be a list when treat_as_element is False.")
    elif treat_as_element:
        value = [value]

    if not in_place:
        document = copy.deepcopy(document)
    return _nested_update(document=document, key=key, value=value)


def _nested_update(document, key, value):
    """
    Method to update a key->value pair in a nested document.
    If the number of passed values is less than the number of key matches
    when scanning for updates, use last value as default.
    Args:
        document: Might be List of Dicts (or) Dict of Lists (or)
            Dict of List of Dicts etc...
        key (str): Key to update the value
        value (list): value(s) which should be used for replacement purpouse
    Return:
        Returns a document that has updated key, value pair.
    """
    if isinstance(document, list):
        for list_items in document:
            _nested_update(document=list_items, key=key, value=value)
    elif isinstance(document, dict):
        for dict_key, dict_value in document.items():
            if dict_key == key:
                document[key] = value[0]
                if len(value) > 1:
                    value.pop(0)
            _nested_update(document=dict_value, key=key, value=value)
    return document


def nested_alter(
    document,
    key,
    callback_function=None,
    function_parameters=None,
    conversion_function=None,
    wild_alter=False,
    in_place=False,
):
    """
    Method to alter all values of the occurences of the key "key".
    The provided callback_function is used to alter the scalar values
    Args:
        document: Might be List of Dicts (or) Dict of Lists (or)
            Dict of List of Dicts etc...
        key: Key to update the value
        callback_function :A callback function which alters a scalar value
            HINT: You should be aware that not every element might be of
            the same type, please check this in your function!
        function_parameters (list):
            If the callback_function has additional input arguments except
            the scalar value, please specify those in this list.
        conversion_function: A conversion function like str() which should be
            applied to every found value before it is passed to the
            "callback_function"
        wild_alter: Find matching elements via wild-match by the given keys
            and alter those.
        HINT: Keep in mind that the wild-match might return unexpected types!
        in_place (bool):
            True: modify the dict in place;
            False: create a deep copy of the dict and modify it
            Defaults to False
    Return:
        Returns a document that has updated key, value pair.
    """
    # check if a list or scalar value is provided and create a list from
    # the scalar value
    # check the length of the list and provide it to _nested_update
    if isinstance(key, list):
        key_len = len(key)
    else:
        key = [key]
        key_len = len(key)

    if not in_place:
        document = copy.deepcopy(document)
    return _nested_alter(
        document=document,
        keys=key,
        callback_function=callback_function,
        function_parameters=function_parameters,
        conversion_function=conversion_function,
        wild_alter=wild_alter,
        in_place=in_place,
        key_len=key_len,
    )


def _call_callback(
    value_list, callback_function, function_parameters, conversion_function
):
    """
    internal helper to call the callback function
    """
    return_list = []
    # loop over all values
    for value in value_list:
        # apply the conversion function
        if conversion_function is not None:
            value = conversion_function(value)
        # if functions arguments are present, expand the list to variables
        # via the magic operator *
        if function_parameters:
            trans_val = callback_function(value, *function_parameters)
        else:
            trans_val = callback_function(value)
        # append the transformed element to the list
        return_list.append(trans_val)
    return return_list


def _nested_alter(
    document,
    keys,
    callback_function,
    function_parameters,
    conversion_function,
    wild_alter,
    in_place,
    key_len,
):
    # return data if no callback_function is provided
    if callback_function is None:
        warnings.warn("Please provide a callback_function to nested_alter().")
        return document

    # iterate over all given keys in the list
    for key in keys:
        # try to find the key:
        findings = nested_lookup(key, document, with_keys=True, wild=wild_alter)
        for k, v in findings.items():
            trans_val = _call_callback(
                v, callback_function, function_parameters, conversion_function
            )
            # use the transformed value and apply the update to the key
            # (dont treat the lists as elements here)
            document = nested_update(
                document, k, trans_val, in_place=in_place, treat_as_element=False
            )

    return document
