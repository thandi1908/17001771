from pathlib import Path
import pytest
from glaciers import Glacier, GlacierCollection


#glaciercollection to be used in pytest
@pytest.fixture
def glaciercol():
    return GlacierCollection(Path("sheet-A.csv"))



# test glacier collection object
def test_GlacierCollect(file_path = ""):
    with pytest.raises(TypeError):
        GlacierCollection(file_path)

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

# test read_mass_balance

# test find_nearest

# test filter_by_code 

# test sort_by_latest_mass_balance

# test summary
