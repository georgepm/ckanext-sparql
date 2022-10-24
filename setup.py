from setuptools import find_packages, setup

version = "0.1"

setup(
    name="ckanext-sparql",
    version=version,
    description="Sparql_Point",
    long_description="",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="",
    author="Jorge Pantoja",
    author_email="jorgepantojam@gmail.com",
    url="http://data.upf.edu",
    license="AGPL",
    packages=find_packages(),
    namespace_packages=["ckanext", "ckanext.sparql"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ckan",
        "simplejson",
        "SPARQLWrapper",
    ],
    entry_points="""
        [ckan.plugins]
    # Add plugins here, eg
    # myplugin=ckanext.sparql:PluginClass
    sparql_interface = ckanext.sparql.plugin:SparqlPlugin
    """,
)
