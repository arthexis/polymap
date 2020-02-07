# Module under test
from polymap import *


def test_create_from_kwargs():
    poly = PolyMap(hello="world")
    assert poly["hello"] == "world"


def test_create_from_mapping():
    poly = PolyMap({"hello": "world"})
    assert poly["hello"] == "world"


def test_setitem_with_group_check():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    assert poly["cat"] == "tom"
    assert "animal" in poly.groups()


def test_items_by_group():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    assert set(poly.items("plant")) == {("marigold", "flowey")}


def test_keys_by_group():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    assert set(poly.keys("plant")) == {"marigold"}


def test_values_by_group():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    assert set(poly.values("plant")) == {"flowey"}


def test_iter_over_keyed_group():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    assert set(poly.groups("marigold")) == {"plant"}


def test_create_defaultpolymap():
    poly = DefaultPolyMap(int)
    assert poly["test"] == 0


def test_iter_grouped():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    for group, items in poly.grouped():
        assert group in ("animal", "plant")
        if group == "animal":
            assert set(items) == {("cat", "tom")}
        elif group == "plant":
            assert set(items) == {("marigold", "flowey")}


def test_clear_by_group():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["marigold", "plant"] = "flowey"
    poly.clear("plant")
    assert set(poly.keys()) == {"cat"}


def test_update():
    poly1 = PolyMap()
    poly1["cat", "animal"] = "tom"
    poly2 = PolyMap()
    poly2["marigold", "plant"] = "flowey"
    poly1.update(poly2)
    assert "marigold" in poly1.keys()
    assert "plant" in poly1.groups()


def test_equals():
    poly1 = PolyMap()
    poly1["cat", "animal"] = "tom"
    poly2 = PolyMap()
    poly2["cat", "animal"] = "tom"
    assert poly1 == poly2


def test_copy_equals():
    poly1 = PolyMap()
    poly1["cat", "animal"] = "tom"
    poly2 = poly1.copy()
    assert set(poly1.groups()) == set(poly2.groups())
    assert poly1 == poly2



def test_ungroup_all_groups():
    poly = PolyMap()
    poly["cat", "animal"] = "tom"
    poly["dog", "animal"] = "odie"
    poly["dog", "show"] = "garfield"
    poly.ungroup("dog")
    assert set(poly.groups("dog")) == set()
    assert set(poly.groups()) == {"animal"}


def test_group_key():
    poly = PolyMap()
    poly["cat"] = "tom"
    poly.group("cat", "animals")
    assert set(poly.groups("cat")) == {"animals"}
