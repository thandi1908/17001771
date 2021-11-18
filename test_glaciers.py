from pathlib import Path
import pytest
from glaciers import Glacier, GlacierCollection


# only created when called by a test fucntion
@pytest.fixture
def glaciercol():
    return GlacierCollection(Path("sheet-A.csv"))

@pytest.fixture
def full_glac_col():
    collection = GlacierCollection(Path("sheet-A.csv"))
    collection.read_mass_balance_data(Path("sheet-EE.csv"))
    return collection



#test glacier object (Negative tests)
@pytest.mark.parametrize("err,glacier_id,name,unit,lat,lon,code",
 [
     (ValueError, "123456", "Glacier1","AG",10,10, 123),
     (TypeError, "12345", 2, "AG",10,-10, 123 ), (TypeError, "12345", "Glacier2", 2, -10,-10, 123),
     (ValueError, "12345", "Glacier2", "ag", -10, -10, 123), (ValueError, "12345", "Glacier2", "AG", -100, -10, 123),
     (ValueError, "12345", "Glacier2", "ag", -10, 200, 123), (ValueError, "12345", "Glacier2", "ag", -10, -10, 1234),
     (ValueError, "12345", "Glacier2", "ag", -10, -10, "453")
  ])
def test_glacier(err, glacier_id, name, unit, lat, lon, code):
    with pytest.raises(err):
        Glacier(glacier_id, name, unit, lat, lon, code) 

# test add_mass_balance
def test_add_mass_balace(glaciercol):
    # test function rejects full measurement after partial measurements have been added
    glaciercol.glaciers["04532"].add_mass_balance_measurement("2020",20, True)
    glaciercol.glaciers["04532"].add_mass_balance_measurement("2020",10, True)
    glaciercol.glaciers["04532"].add_mass_balance_measurement("2020",5, True)
    glaciercol.glaciers["04532"].add_mass_balance_measurement("2020",70, False)

    # test function can accept a full measurement
    glaciercol.glaciers["01346"].add_mass_balance_measurement("2020", -30, False)

    assert glaciercol.glaciers["04532"].mass_balance["2020"]["mass_balance"] == 35
    assert glaciercol.glaciers["01346"].mass_balance["2020"]["mass_balance"] == -30


# test read_mass_balance

# test find_nearest

# test filter_by_code (Negative tests)
@pytest.mark.parametrize("err, code_pattern",
[
    (TypeError,[123] ), (ValueError, "???"),
    (ValueError, "123?"), (ValueError, "1234"),
    (ValueError, "abd"), (ValueError, 8765),
    (ValueError, 000 ), (ValueError, "000")
])
def test_filter_by_code_neg(err, code_pattern, full_glac_col):
    with pytest.raises(err):
        full_glac_col.filter_by_code(code_pattern)

# test filter_by_code (Positive tests)
@pytest.mark.parametrize("code_pattern, expected_result",
 [
     ("123",[]), (517, ["BAJO DEL PLOMO"]),
     ("?34", ["ALERCE", "PIEDRAS BLANCAS", "TORRE", "FJALLSJOKULL BY BREIDAMERKURFJALL",
      "FJALLSJOKULL BY GAMLASEL", "FJALLSJOKULL FITJAR", "GIGJOKULL", "ARTESONRAJU"]),
      ("48?", ["DIMDAL-FRUKOSTTINDBREEN", "FLATISVATNET", "MEMORGEBREEN", "NORDFJORDBREEN", "NORTHERN PART"])
 ])
def test_filter_by_code_postive(code_pattern, expected_result,full_glac_col):
    assert full_glac_col.filter_by_code(code_pattern) == expected_result

# test sort_by_latest_mass_balance (positive)
@pytest.mark.parametrize("n,reverse,expected_result",
 [
     (5, True, ["BROWN SUPERIOR","CONCONTA NORTE", "AGUA NEGRA", "SHAUNE GARANG", "DE LOS TRES"]),
     (1, False, ["DE LOS TRES"]),
      (5, False, ['DE LOS TRES', 'SHAUNE GARANG', 'AGUA NEGRA', 'CONCONTA NORTE', 'BROWN SUPERIOR'] ),
      (2, True, ["BROWN SUPERIOR","CONCONTA NORTE"])

 ])
def test_sort_by_lastest_mass_balance_pos(n, reverse, expected_result,glaciercol):
    collection = glaciercol
    collection.read_mass_balance_data(Path("sheet-test.csv"))
    sort = collection.sort_by_latest_mass_balance(n,reverse)
    sort_names = [i.name for i in sort]
    print(sort_names)

    assert sort_names == expected_result

# test sort by latest mass balance (Negative)
@pytest.mark.parametrize("n,reverse,err",
[
    (-1, False, ValueError),
     ("40", False, TypeError ),
     (500, False, ValueError)
])
def test_sort_by_latest_mass_balance_neg(n, reverse, err, glaciercol):
    collection = glaciercol
    collection.read_mass_balance_data(Path("sheet-test.csv"))

    with pytest.raises(err):
        sort = collection.sort_by_latest_mass_balance(n,reverse)

# test find nearest (Negative)
@pytest.mark.parametrize("err,lat,lon,n",
 [
    (ValueError, -90.6,-90, 5 ),
    (ValueError, -90,200,5),
    (ValueError,-90, 90, 20000000),
    (TypeError, -90, 100, "12"),
    (AssertionError, "-90", 100, 12),
    (AssertionError,-90, "130", 12),
    (ValueError, -90, - 90, -90)
 ])
def test_find_nearest_neg(err,lat,lon,n,glaciercol):
    with pytest.raises(err):
        glaciercol.find_nearest(lat,lon,n)



# test find nearest (Positive)
def test_find_nearest_pos(glaciercol):
    assert glaciercol.find_nearest(-30.16490,-69.80940, n=1) == ["AGUA NEGRA"]

# test glacier collection object
def test_GlacierCollect(file_path = ""):
    with pytest.raises(TypeError):
        GlacierCollection(file_path)