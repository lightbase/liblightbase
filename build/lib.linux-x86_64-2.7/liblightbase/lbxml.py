# -*- coding: utf-8 -*-
from xml.dom import minidom
import lbtypes, lbmetaclass

def xml_to_class(xml):
    """ Converts XML to class.
        XML is a string with the XML file content
        returns the respective class
    """
    doc = minidom.parseString(xml)
    class_structure = doc.childNodes[0]
    class_name = class_structure.getAttribute('name').encode('utf-8')
    attrs = [ get_attr(attr) for attr in class_structure.childNodes if attr.nodeName != '#text']
    return lbmetaclass.generate_class(class_name, attrs)

def xml_to_object(xml):
    """ Converts XML to object.
        XML is a string with the XML file content
        return the respective object
    """
    cls = xml_to_class(xml)
    obj = cls()
    
    doc = minidom.parseString(xml)
    doc = doc.childNodes[0]
    
    for childNode in doc.childNodes:
        if not hasattr(childNode,'getAttribute'):
            continue
        name = childNode.getAttribute('name')
        field = getattr(obj,name,None)
        if field is None:
            continue
        field.__read_xml__(childNode.childNodes)
    
    return obj 
    
    
def get_attr(attr):
    """
        Read the XML file recursively, 
        returning the respective lbtype
    """
    attr_type = attr.nodeName.encode('utf-8')
    if attr_type == '#text':
        return
    attr_name = attr.getAttribute('name').encode('utf-8')
    
    lbtype = lbtypes.get_lbtype(attr_type, allow_meta=True)
    
    if lbtypes.is_lbtype(lbtype):
        return { 'name': attr_name, 'type': attr_type }
    
    inner_type = attr.getAttribute('type').encode('utf-8')
    
    if inner_type:
        inner_lbtype = lbtypes.get_lbtype(inner_type, allow_meta=True)
        if lbtypes.is_lbtype(inner_lbtype):
            return { 'name': attr_name, 'type': lbtype(inner_lbtype) }
    
    inner_types = [ get_attr(attr) for attr in attr.childNodes if attr.nodeName != '#text']
    
    return { 'name': attr_name, 'type': lbtype(inner_types) }
    
def object_to_xml(obj, pretty=True, xml_url="http://lightbase.cc/object", xml_name="object"):
    """ Generate a XML from a LBMetaClass object
        returns a XML as string
    """
    doc = minidom.Document()
    doc.appendChild(doc.createElementNS(xml_url,xml_name))
    doc.childNodes[0].setAttribute('name',obj.__class__.__name__)
    for attr in [obj.__get_lbtype_attr__(key['name']) for key in obj._structure]:
        doc.childNodes[0].appendChild(attr.__xml__(doc))
    if pretty:
        return doc.toprettyxml()

    return doc.toxml()
    
def class_to_xml(cls, pretty=True, xml_url="http://lightbase.cc/class", xml_name="class"):
    """ Generate a XML from a LBMetaClass class
        returns a XML as string
    """
    obj = cls()
    return object_to_xml(obj, pretty, xml_url, xml_name)

