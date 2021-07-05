from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    改进版本，支持 title__author 这种双下划线形式的fields
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        def _remove_fields(fields, field_names):
            if field_names is not None:
                allowed_fields = [field.split("__")[0] for field in field_names]
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(allowed_fields)
                existing = set(fields)
                for field_name in existing - allowed:
                    fields.pop(field_name)

            childs = defaultdict(list)
            for field in field_names:
                if len(field.split("__")) > 1:
                    childs[field.split("__")[0]].append(
                        "__".join(field.split("__")[1:])
                    )

            for key, value in childs.items():
                if isinstance(fields[key], serializers.ListSerializer):
                    _remove_fields(fields[key].child.fields, value)
                else:
                    if hasattr(fields[key], "fields"):
                        _remove_fields(fields[key].fields, value)

            # Don't pass the 'fields' arg up to the superclass

        def _delete_fields(fields, field_names):
            if field_names is not None:
                allowed_fields = [field.split("__")[0] for field in field_names]
                # Drop any fields that are not specified in the `fields` argument.
                allowed = set(allowed_fields)
                for field_name in allowed_fields:
                    fields.pop(field_name)

            childs = defaultdict(list)
            for field in field_names:
                if len(field.split("__")) > 1:
                    childs[field.split("__")[0]].append(
                        "__".join(field.split("__")[1:])
                    )

            for key, value in childs.items():
                if isinstance(fields[key], serializers.ListSerializer):
                    _delete_fields(fields[key].child.fields, value)
                else:
                    if hasattr(fields[key], "fields"):
                        _delete_fields(fields[key].fields, value)

            # Don't pass the 'fields' arg up to the superclass

        _fields = kwargs.pop("fields", None)
        _exclude_fields = kwargs.pop("exclude_fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        # assert _fields or _exclude_fields, 'exclude_fields,fields 只支持一个'

        if _fields:
            _remove_fields(self.fields, _fields)

        if _exclude_fields:
            _delete_fields(self.fields, _exclude_fields)


# class DynamicFieldsModelSerializer(serializers.ModelSerializer):
#     """
#     A ModelSerializer that takes two additional arguments
#     `fields` that controls which fields should be displayed.
#     `exclude_fields` that controls which fields to be excluded.
#     href: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
#     """
#
#     def __init__(self, *args, **kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop("fields", None)
#         exclude_fields = kwargs.pop("exclude_fields", None)
#
#         # Instantiate the superclass normally
#         super().__init__(*args, **kwargs)
#
#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#
#         if exclude_fields is not None:
#             # Drop any fields that are specified in the `exclude_fields` argument.
#             exclude = set(exclude_fields)
#             existing = set(self.fields)
#             for field_name in existing.intersection(exclude):
#                 self.fields.pop(field_name)
