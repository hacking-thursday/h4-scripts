import sys
import os
import xml
import tempfile

root_path = os.path.abspath(os.path.join( os.path.dirname(__file__), "..") )
sys.path.append(os.path.join(root_path ))
sys.path.append(os.path.join(root_path, '3rd'))

import common
from common import *

def html2xml(the_html):
    result = ""
    htmlfile = tempfile.mktemp()
    xmlfile = tempfile.mktemp()
    string2file(the_html, htmlfile)
    os.system("tidy -q -asxhtml -numeric -utf8 < " + htmlfile + " > " + xmlfile)
    result = file2string(xmlfile)
    os.system("rm " + htmlfile)
    os.system("rm " + xmlfile)

    return result


def get_etherpad_content_body(URL):
    htmlfile = tempfile.mktemp()

    ret = os.system("wget -O " + htmlfile + " " + URL)
    if ret == 0:
        the_html = file2string(htmlfile)
    else:
        the_html = None
    os.system("rm " + htmlfile)

    result = the_html

    return result


def indent(elem, level=0):
  i = "\n" + level*"  "
  print( "=============" )
  print( elem )
  print( elem.attrib )
  print( elem.tag    )
  print( elem.tail   )
  print( elem.text   )
  print( "=============" )

  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i



def get_wikidot_content_body_fork(URL):
    htmlfile = tempfile.mktemp()
    xhtmlfile = tempfile.mktemp()

    os.system("wget -O " + htmlfile + " " + URL)
    the_html = file2string(htmlfile)
    the_xhtml = html2xml( the_html )
    string2file( the_xhtml, xhtmlfile )

    namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}
    doc = xml.etree.ElementTree.parse( xhtmlfile )
    res = doc.findall(".//xhtml:div[@id='page-content']", namespaces = namespaces )
    xml_obj = res[0]
    
    indent( xml_obj )
    res_txt = xml.etree.ElementTree.dump( xml_obj )

    os.system("rm " + xhtmlfile)
    os.system("rm " + htmlfile)

    result = res_txt

    return result

URL = "http://www.hackingthursday.org/invite"
print( get_wikidot_content_body_fork(URL) )
