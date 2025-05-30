import io, textwrap

from jvasseur.packaging import feed

def test_from_xml_empty():
    interface = feed.from_xml(io.StringIO(textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface"/>
    """).lstrip()))

    assert len(interface.children) == 0

def test_from_xml_one_implementation():
    interface = feed.from_xml(io.StringIO(textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">
            <implementation id="1" released="2025-05-19" version="1"/>
        </interface>
    """).lstrip()))

    assert len(interface.children) == 1
    assert interface.children[0].id == '1'
    assert interface.children[0].released == '2025-05-19'
    assert interface.children[0].version == '1'
