import textwrap

from jvasseur.packaging.feed import Archive, Interface, Implementation
from jvasseur.packaging.xml import to_xml

def test_to_xml_empty():
    interface = Interface()

    assert to_xml(interface, indent='    ').read() == textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface"/>
    """).lstrip()

def test_to_xml_one_implementation():
    interface = Interface()
    interface.append(Implementation(id='1', released='2025-05-19', version='1'))

    assert to_xml(interface, indent='    ').read() == textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">
            <implementation id="1" released="2025-05-19" version="1"/>
        </interface>
    """).lstrip()

def test_to_xml_one_implementation_with_archive():
    interface = Interface()
    interface.append(Implementation(
        Archive(href="http://example.com", size=0),
        id='1',
        released='2025-05-19',
        version='1',
    ))

    assert to_xml(interface, indent='    ').read() == textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">
            <implementation id="1" released="2025-05-19" version="1">
                <archive href="http://example.com" size="0"/>
            </implementation>
        </interface>
    """).lstrip()
