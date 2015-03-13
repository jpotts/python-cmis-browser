This is a basic [CMIS](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=cmis) browser implemented using [Pyramid](http://www.pylonsproject.org/projects/pyramid/about) and [cmislib](http://chemistry.apache.org/python/cmislib.html). It's meant as a simple example to show one way to use Python to work with objects that live in a CMIS repository.

If you want to see it in action, watch this short screencast:

<a href='http://www.youtube.com/watch?feature=player_embedded&v=B9nV3uUb0Hw' target='_blank'><img src='http://img.youtube.com/vi/B9nV3uUb0Hw/0.jpg' width='425' height=344 /></a>

Refer to the InstallDocs to learn how to run it on your machine. All you need is Python, setuptools, and virtualenv. The framework dependencies and cmislib will be installed for you automatically.

## Interoperability ##

This is known to work with [Alfresco 4.0.d Community Edition](http://wiki.alfresco.com/wiki/Download_and_Install_Alfresco) and [OpenCMIS](http://chemistry.apache.org/java/opencmis.html) 0.7 InMemory Repository, but it should work with any CMIS-compliant repository because it relies on cmislib, which is spec-compliant.

The exception to that is the global navigation. It has two links in it, one called "Sites" and the other called "Repository" that map to Alfresco concepts. The "Sites" link will work with any repository that has a folder named "Sites" in the root folder. The "Repository" link will work with any repository.

## Limitations ##

This is meant as a barebones app for learning purposes or for people who just need to provide quick-and-dirty, unauthenticated access to the objects in their CMIS repository. At the moment, it is limited to CRUD functions on folders and documents. It does not support checkin/checkout, versioning, renditions, associations, permissions, or any other CMIS goodness beyond simply creating folders and files. All of that could easily be added, though, because cmislib supports it.
