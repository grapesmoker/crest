# cREST - the compact REST interface

cREST is a small module to make writing code that accesses REST interfaces simple. It encapsulates the code to access REST APIs behind three classes, `RESTInterface`, `Client`, and `RESTCall`. The `Client` maintains state like authorization and tokens as well as the host of the interface, while the `RESTInterface` knows about how to interact with the API.

## Example:

```python
from crest.client import Client
from crest.builder import RESTInterface, Get, GetPost

class MyNiceInterface(RESTInterface):
  
  api_base = 'api'
  
  users = Get('users')
  user = GetPost('users/{id}')
  
client = Client('https://reqres.in')
my_interface = MyNiceInterface(client)

my_interface.users.get()  # returns a list of users
my_interface.user.get(id=2)  # returns user with id = 2
my_interface.user.post(params={'name': 'nobody'})  # posts a user
```

## JSONSchema extensions

cREST also implements a few extensions to the [jsonschema](https://github.com/Julian/jsonschema) package, which is itself an implementation of the spec of [JSON Schema](https://json-schema.org). In particular, cREST allows you to nest schemas and appropriately resolves definitions to account for the nesting structure, which ordinary JSONSchema does not do. For an example, consider the following situations:

```python
from crest.schema import JSONSchema

inner_schema = JSONSchema({
    'title': 'inner_schema',
    'type': 'object',
    'properties': {
        'point': {
            'type': 'object',
            '$ref': '#/definitions/point'
        }
    },
    'definitions': {
        'point': {
            'type': 'object',
            'properties': {
                'x': {
                    'type': 'number'
                },
                'y': {
                    'type': 'number'
                }
            }
        }
    }
})

outer_schema = JSONSchema({
    'title': 'outer_schema',
    'type': 'object',
    'properties': {
        'inner_schema': {
            'type': 'object',
            '$ref': '#/definitions/inner_schema'
        }
    },
    'definitions': {
        'inner_schema': inner_schema
    }
})
``` 

Here, the inner schema is nested within the outer schema. However, if you tried this in pure `jsconschema`, you would get a resolver error because the definitions in the inner schema are referenced to the top of its document object, which is `inner_schema`, while the definitions in the outer schema referenced to the top of _its_ document object, which is of course `outer_schema`. Thus, the path for the inner schema references is incorrect.

cREST implements a relabeling mechanism which crawls the of the outermost schema from the top level and sets the definitions to their correct references. Thus, if you printed out the outer schema after its `adjust_references` method has been called (which it is by default on initialization, via the `recompute_refs` parameter), you would now see:

```json
{
    "title": "outer_schema",
    "type": "object",
    "properties": {
        "inner_schema": {
            "type": "object",
            "$ref": "#/definitions/inner_schema"
        }
    },
    "definitions": {
        "inner_schema": {
            "title": "inner_schema",
            "type": "object",
            "properties": {
                "point": {
                    "type": "object",
                    "$ref": "#/definitions/inner_schema/definitions/point"
                }
            },
            "definitions": {
                "point": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number"
                        },
                        "y": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }
}
```

Note how the `$ref` inside the `inner_schema` contains the proper location of the definition of the `point` object. Schemas can be nested indefinitely, but not mutually-recursively (yet). Also, when you nest one schema inside another, the initializer makes a copy of the underlying dict, so you don't have to worry about your internally nested schema being modified.