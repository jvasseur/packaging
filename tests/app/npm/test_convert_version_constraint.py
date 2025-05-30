from jvasseur.packaging.app.npm import convert_version_constraint

def test_convert_version_constraint():
    assert convert_version_constraint('^18.17.1 || ^20.10.0 || >=22.11.0') == '18.17.1..!19 | 20.10.0..!21 | 22.11.0..'
