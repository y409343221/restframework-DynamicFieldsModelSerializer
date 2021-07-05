## Example

```python
>>> class UserSerializer(DynamicFieldsModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ['id', 'username', 'email', "title__author"]
>>>
>>> print(UserSerializer(user))
{'id': 2, 'username': 'jonwatts', 'email': 'jon@example.com',"title__author": "xxx"}
>>>
>>> print(UserSerializer(user, fields=('id', 'email')))
{'id': 2, 'email': 'jon@example.com'}
>>> print(UserSerializer(user, exclude_fields=('id', "title__author")))
{'username': 'jonwatts', 'email': 'jon@example.com'}
```





```
>>> class UserSerializer(DynamicFieldsModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ['id', 'username', 'email']
>>>
>>> print(UserSerializer(user))
{'id': 2, 'username': 'jonwatts', 'email': 'jon@example.com'}
>>>
>>> print(UserSerializer(user, fields=('id', 'email')))
{'id': 2, 'email': 'jon@example.com'}
>>> print(UserSerializer(user, exclude_fields=('id')))
{'username': 'jonwatts', 'email': 'jon@example.com'}

```