import textwrap

from jvasseur.packaging import feed

def test_to_xml_empty():
    interface = feed.Interface()

    assert feed.to_xml(interface, indent='    ').read() == textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface"/>
    """).lstrip()

def test_to_xml_one_implementation():
    interface = feed.Interface()
    interface.append(feed.Implementation(id='1', released='2025-05-19', version='1'))

    assert feed.to_xml(interface, indent='    ').read() == textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">
            <implementation id="1" released="2025-05-19" version="1"/>
        </interface>
    """).lstrip()
