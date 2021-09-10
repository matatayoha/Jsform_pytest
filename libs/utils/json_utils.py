import json
import re
from requests.structures import CaseInsensitiveDict
from deepdiff import DeepDiff
from deepdiff.model import PrettyOrderedSet
import jsonpath


class JsonUtils:

    # verify the json string is valid json
    @classmethod
    def is_json(cls, my_json):
        try:
            json.loads(my_json)
        except Exception:
            return False
        return True

    @classmethod
    def json_to_object(cls, my_class_json, my_class):
        my_class_rebuild = json.loads(my_class_json)
        # my_class = My_Class()
        my_class.__dict_ = my_class_rebuild
        return my_class

    @classmethod
    def object_to_json(cls, my_class):
        return json.loads(json.dumps(my_class.__dict__))

    @classmethod
    def dict_generator(cls, indict, pre=None):
        pre = pre[:] if pre else []
        if isinstance(indict, list):
            if len(indict) == 0:
                yield pre
            else:
                i = 0
                for v in indict:
                    for d in JsonUtils.dict_generator(v, pre + [str(i)]):
                        yield d
                    i = i + 1
        elif isinstance(indict, dict) or isinstance(indict, CaseInsensitiveDict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    if len(value) == 0:
                        yield pre+[key, '{}']
                    else:
                        for d in JsonUtils.dict_generator(value, pre + [key]):
                            yield d
                elif isinstance(value, list):
                    if len(value) == 0:
                        yield pre+[key, '[]']
                    else:
                        i = 0
                        for v in value:
                            for d in JsonUtils.dict_generator(v, pre + [key] + [str(i)]):
                                yield d
                            i = i + 1
                elif isinstance(value, tuple):
                    if len(value) == 0:
                        yield pre+[key, '()']
                    else:
                        for v in value:
                            for d in JsonUtils.dict_generator(v, pre + [key]):
                                yield d
                else:
                    yield pre + [key, value]
        else:
            yield indict

    @classmethod
    def get_value_by_path(cls, json, json_path):
        """
        we know a item path in a json, try to get its value through the path
        @param json:
        @param json_path:
        @return:
        """
        json_path = str(json_path).replace("root", "$").replace("['", ".").replace("']", "")
        return jsonpath(json, json_path)

    @classmethod
    def dict_compare(cls, json_self, json_target, ignore_order=False, ignore_string_case=False, exclude_paths=None):
        """
        Compare the differences between two jsons
        @param json_self: the json str should be come from the API response
        @param json_target:  it is the target json we use to compare, it is build as expected by your
        @param ignore_order: ignore the order for list part in the json
        self
        @return:
        """
        errors = list()
        differences = DeepDiff(json_target, json_self, ignore_order=ignore_order, ignore_string_case=ignore_string_case,
                               exclude_paths=exclude_paths)
        # usually we don't check the extra part, but we will be strict with the missing part in the json
        item_added = differences["dictionary_item_added"] if "dictionary_item_added" in differences else []
        item_removed = differences["dictionary_item_removed"] if "dictionary_item_removed" in differences else []
        values_changed = differences["values_changed"] if "values_changed" in differences else {}
        for item in item_removed:
            value = cls.get_value_by_path(json_target, item)
            if value[0] is not None:
                errors.append("Field in the response body is missing: " + str(item))
        for key, value in values_changed.items():
            pattern = "^" + str(value["old_value"]) + "$"
            source = str(value["new_value"])
            ignore_string_case = re.I if ignore_string_case else 0
            if not re.match(pattern, source, flags=ignore_string_case):
                errors.append("Field in the response body is not matching: " + str(key) + ", expected: < " +
                              str(value["old_value"]) + " > but actually: < " + str(value["new_value"]) + " >")

        if len(errors) > 0:
            raise AssertionError(errors)