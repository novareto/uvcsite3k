"""

Rest API
========

Setup
-----
First start with an instance of UAZFolder

  >>> import grok
  >>> grok.grok('uvcsite.browser.tests.fixtures.usermanagement')
  >>> grok.grok(dottedname)

  >>> root = layer.getRootFolder()
  >>> app = layer.create_application('app')

  >>> folder = UAZFolder()
  >>> folder
  <...api_json.UAZFolder object at ...>

Add the folder to the RootFolder!

  >>> app['uaz'] = folder
  >>> app['uaz']
  <...api_json.UAZFolder object at ...>

Rest Operations
---------------


POST
----

Ok there is no meaningful post method implemented yet!

  >>> auth_header = "Basic 0101010001:passwort"

GET
---

So start with a GET Request of the Container! Ok are no
content objects in it so we only get an empty container listing.

  >>> browser = layer.new_browser('http://localhost/app')
  >>> browser.handleErrors = False 
  >>> browser.addHeader('Authorization', auth_header)
  >>> response = browser.open("http://localhost/++rest++jsonapi/app/uaz")

  >>> import json
  >>> print(json.dumps(json.loads(browser.contents), indent=4, sort_keys=True))
  {
      "id": "uaz",
      "items": []
  }

Now let's add objects to the container and see the GET Request again

  >>> uaz = Unfallanzeige()
  >>> uaz.title = "Mein Unfall"
  >>> uaz.name = "Christian Klinger"
  >>> uaz.age = 29

  >>> uaz1 = Unfallanzeige()
  >>> uaz1.title = "Unfall von Lars"
  >>> uaz1.name = "Lars Walther"
  >>> uaz1.age = 39

One item in the container!

  >>> app['uaz']['christian'] = uaz
  >>> response = browser.open("http://localhost/++rest++jsonapi/app/uaz")
  >>> print(json.dumps(json.loads(browser.contents), indent=4, sort_keys=True))
  {
      "id": "uaz",
      "items": [
          {
              "@url": "http://www.google.de",
              "author": "0101010001",
              "datum": "...",
              "id": "christian",
              "meta_type": "Unfallanzeige",
              "status": "Entwurf",
              "titel": "Mein Unfall"
          }
      ]
  }


The object itself has also a get method

  >>> response = browser.open(
  ...     "http://localhost/++rest++jsonapi/app/uaz/christian")
  >>> print(json.dumps(json.loads(browser.contents), indent=4, sort_keys=True))
  {
      "age": 29,
      "name": "Christian Klinger",
      "title": "Mein Unfall"
  }

More items in the container!

  >>> root['uaz']['lars'] = uaz1
  >>> response = browser.open("http://localhost/++rest++jsonapi/app/uaz")
  >>> print(json.dumps(json.loads(browser.contents), indent=4, sort_keys=True))
  {
      "id": "uaz", 
      "items": [
          {
              "@url": "http://www.google.de", 
              "author": "0101010001", 
              "datum": "...", 
              "id": "christian", 
              "meta_type": "Unfallanzeige", 
              "status": "Entwurf", 
              "titel": "Mein Unfall" 
          },
          {
              "@url": "http://www.google.de", 
              "author": "0101010001", 
              "datum": "...", 
              "id": "lars", 
              "meta_type": "Unfallanzeige", 
              "status": "Entwurf", 
              "titel": "Unfall von Lars" 
          }
      ]
  }


PUT
---

A Valid uaz_xml file!

  >>> uaz_xml = '''
  ...     {
  ...         "age": 30,
  ...         "name": "Christian Moser",
  ...         "title": "Mein Unfall JSON"
  ...      }
  ...    '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz', uaz_xml, AUTHORIZATION=auth_header)

  >>> print format(response)
  {
      "id": "Unfallanzeige",
      "name": "Unfallanzeige",
      "result": "success"
  }

We should get this document in our container

  >>> uaz = root['uaz']['Unfallanzeige']
  >>> uaz
  <uvcsite.tests.functional.content.api_json.Unfallanzeige object at ...>

  >>> print uaz.name
  Christian Moser

  >>> print uaz.age
  30

We should now have 3 objects in our container!

  >>> len(root['uaz'])
  3

Invalid uaz_xml file!

  >>> uaz_json_with_error = '''
  ... {
  ...       "title": "Unfallanzeige",
  ...       "name": "CK",
  ...       "age": "thirty"
  ... }
  ... '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz',
  ... uaz_json_with_error, AUTHORIZATION=auth_header)

  >>> result = response.getBody()
  >>> print result
  [{"field": "age", "message": "Object is of wrong type."}]


An invariant uaz_xml file

  >>> uaz_json_with_invariant = '''
  ... {
  ...       "title": "Mein Unfall",
  ...       "name": "hans",
  ...       "age": 10
  ... }
  ... '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz',
  ...  uaz_json_with_invariant, AUTHORIZATION=auth_header)
  >>> print response.getBody()
  [{"text": "Invariant: This combination of name and age is not valid"}]

"""


import grok
import uvcsite.content.interfaces
import uvcsite.content.components
import uvcsite.content.directive

from zope.schema import TextLine, Int
from zope.interface import Invalid, invariant


class IUnfallanzeige(uvcsite.content.interfaces.IContent):
    name = TextLine(title="Name", max_length=20)
    age = Int(title="Int")

    @invariant
    def no_sample(unfallanzeige):
        if unfallanzeige.name == "hans" and unfallanzeige.age == 10:
            raise Invalid("This combination of name and age is not valid")


@grok.implementer(IUnfallanzeige)
@uvcsite.content.directive.schema(IUnfallanzeige)
class Unfallanzeige(uvcsite.content.components.Content):
    grok.name('Unfallanzeige')


class UAZFolder(uvcsite.content.components.ProductFolder):
    uvcsite.content.directive.contenttype(Unfallanzeige)
