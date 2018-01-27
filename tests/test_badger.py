import pytest
import badger
import uuid
import os
from badger.__main__ import main

def test_render_simple_badge():
    badge = badger.Badge("simple", "badge")
    badge.render()

def test_render_percentage_badge():
    badge = badger.PercentageBadge("percent", 99)
    badge.render()

def test_percentage_bad():
    with pytest.raises(ValueError):
        badger.PercentageBadge("percent", "not a number")

def test_render_range_badge():
    for i in range(0, 50):
        badge = badger.ColorRangeBadge("simple", i, minimum=0, maximum=50)
        badge.render()

def test_save(tmpdir):
    badge = badger.Badge("simple", "badge")
    fn = "test{}.svg".format(uuid.uuid4())
    fn = str(tmpdir.join(fn))    
    badge.save(fn)
    assert os.path.exists(fn)

def test_save_folder_path():
    badge = badger.Badge("simple", "badge")
    fn = "test{}/test.svg".format(uuid.uuid4())
    with pytest.raises(IOError):
        badge.save(fn)

@pytest.mark.skip("Not sure what the correct width should be here. I get different results on CI and locally.")
def test_width_calculation():
    badge = badger.Badge("simple", "badge")
    calculated = badger._calculate_width_of_text("Hello World !")
    assert calculated == 70


# Test some injections

evil_injection = '<image href="https://blacknode.se/cat" height="200" width="200"/>'

def test_validation(tmpdir):
    badge = badger.Badge("simple", evil_injection)
    fn = "test{}.svg".format(uuid.uuid4())
    fn = str(tmpdir.join(fn))
    badge.save(fn)
    assert os.path.exists(fn)
    with open(fn) as _file:
        assert "<image" not in _file.read()

def test_validation_label_color(tmpdir):
    with pytest.raises(ValueError):
        badger.Badge("simple", "badge", label_color=evil_injection)

def test_validation_value_color(tmpdir):
    with pytest.raises(ValueError):
        badger.Badge("simple", "badge", value_color=evil_injection)


# CLI Tests (only checking that the program does not crash)

def test_main_simple():
    main(argv=["simple","badge"])

def test_main_percentage():
    main(argv=["simple","73%","-p"])
    main(argv=["simple","73","-p"])

def test_main_version():
    with pytest.raises(SystemExit):
        main(argv=["-v"])

def test_main_noargs():
    with pytest.raises(SystemExit):
        main()

def test_main_save(tmpdir):
    fn = "test{}.svg".format(uuid.uuid4())
    fn = str(tmpdir.join(fn))   
    main(argv=["simple","badge","-o",fn])

def test_main_save_quiet(tmpdir):
    fn = "test{}.svg".format(uuid.uuid4())
    fn = str(tmpdir.join(fn))   
    main(argv=["simple","badge","-o",fn,"-q"])
