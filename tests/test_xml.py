import io, textwrap

from jvasseur.packaging.feed import Archive, Arg, Category, Command, Description, Environment, ForEach, Homepage, Icon, Interface, Implementation, Name, Publisher, Runner, SplashScreen, Summary
from jvasseur.packaging.xml import from_xml, to_xml

def test_empty_interface():
    interface = Interface(uri='http://example.com/')

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/"/>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_empty_implementation():
    interface = Interface(
        Implementation(id='1', released='2025-05-19', version='1'),
        uri='http://example.com/'
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1"/>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_implementation_with_details():
    interface = Interface(
        Name('test'),
        Summary('testing'),
        Description('for testing'),
        Publisher('the publisher'),
        Homepage('https://example.com'),
        Category('Utility'),
        Icon(type='image/png', href='https://example.com/icon.png'),
        SplashScreen(type='image/png', href='https://example.com/splash.png'),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <name>test</name>
            <summary>testing</summary>
            <description>for testing</description>
            <publisher>the publisher</publisher>
            <homepage>https://example.com</homepage>
            <category>Utility</category>
            <icon href="https://example.com/icon.png" type="image/png"/>
            <splash-screen href="https://example.com/splash.png" type="image/png"/>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_implementation_with_archive():
    interface = Interface(
        Implementation(
            Archive(href='http://example.com', size=0),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <archive href="http://example.com" size="0"/>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_command():
    interface = Interface(
        Implementation(
            Command(name='run', path='bin/run'),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <command name="run" path="bin/run"/>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_command_with_runner():
    interface = Interface(
        Implementation(
            Command(
                Runner(interface='http://example.com/runner.xml'),
                name='run',
                path='bin/run',
            ),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <command name="run" path="bin/run">
                    <runner interface="http://example.com/runner.xml"/>
                </command>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_command_with_arg():
    interface = Interface(
        Implementation(
            Command(
                Arg('--name'),
                Arg('value'),
                name='run',
                path='bin/run',
            ),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <command name="run" path="bin/run">
                    <arg>--name</arg>
                    <arg>value</arg>
                </command>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_command_with_environment():
    interface = Interface(
        Implementation(
            Command(
                Environment(name='PATH', insert='bin', mode='append', separator=':'),
                Environment(name='VERBOSE', value='1', mode='replace'),
                name='run',
                path='bin/run',
            ),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <command name="run" path="bin/run">
                    <environment name="PATH" insert="bin" mode="append" separator=":"/>
                    <environment name="VERBOSE" value="1" mode="replace"/>
                </command>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface

def test_command_with_for_each():
    interface = Interface(
        Implementation(
            Command(
                ForEach(
                    Arg('${item}'),
                    item_from='SOME_VARIABLE',
                ),
                name='run',
                path='bin/run',
            ),
            id='1',
            released='2025-05-19',
            version='1',
        ),
        uri='http://example.com/',
    )

    xml = textwrap.dedent("""
        <?xml version="1.0"?>
        <interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface" uri="http://example.com/">
            <implementation id="1" released="2025-05-19" version="1">
                <command name="run" path="bin/run">
                    <for-each item-from="SOME_VARIABLE">
                        <arg>${item}</arg>
                    </for-each>
                </command>
            </implementation>
        </interface>
    """).lstrip()

    assert to_xml(interface, indent='    ').read() == xml
    assert from_xml(io.StringIO(xml)) == interface
