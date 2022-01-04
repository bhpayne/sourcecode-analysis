To extract the classes and functions of an API, run Doxygen.

Then "Public Member Functions" in the HTML are what is relevant

Doxygen organizes things by classes, so API stuff ends up in `classhello.xml` instead of `hello_8cc.xml` or `hello_8h.xml`

If you look in the XML you can see the `<sectiondef kind="public-func”>` tag which includes various `<memberdef>` tags. These appear to correspond to what you see in the html file under the "Public Member Functions" section. 
The definition and argstring tags contain most if not all of what you want, and you can just ignore the description tags.
