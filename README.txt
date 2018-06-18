=====
cREST - the compact REST interface
=====

cREST is a small module to make writing code that accesses REST interfaces simple. It encapsulates the code to access
REST APIs behind two classes, `RESTInterface` and `Client`. The `Client` maintains state like authorization and tokens
as well as the host of the interface, while the `RESTInterface` knows about how to interact with the API.

Example
=======

    from crest.client import Client
    from crest.builder import RESTInterface, Get, GetPost

    class MyNiceInterface(RESTInterface):

      api_base = 'api'

      users = Get('users')
      user = GetPost('users/{id}')

    client = Clinet('https://reqres.in')
    my_interface = MyNiceInterface(client)

    my_interface.users.get()  # returns a list of users
    my_interface.user.get(id=2)  # returns user with id = 2
    my_interface.user.post(params={'name': 'nobody'})  # posts a user
