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

def test_save():
    badge = badger.Badge("simple", "badge")
    fn = "test{}.svg".format(uuid.uuid4())
    badge.save(fn)
    assert os.path.exists(fn)
    os.remove(fn)

def test_save_folder_path():
    badge = badger.Badge("simple", "badge")
    fn = "test{}/".format(uuid.uuid4())
    with pytest.raises(IOError):
        badge.save(fn)

def test_width_calculation():
    badge = badger.Badge("simple", "badge")
    calculated = badger._calculate_width_of_text("Hello World !")
    assert calculated == 70


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

def test_main_save():
    fn = "test{}.svg".format(uuid.uuid4())
    main(argv=["simple","badge","-o",fn])
    os.remove(fn)

def test_main_save_quiet():
    fn = "test{}.svg".format(uuid.uuid4())
    main(argv=["simple","badge","-o",fn,"-q"])
    os.remove(fn)

