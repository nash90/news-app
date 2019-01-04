import pytest

from news.models import ContentType
from news.models import Category 

test_param = (
  ["name1","descp1","name1", "descp1"],
  ["name2","descp2","name2", "descp2"],
  ["name3","descp3","name3", "descp3"]
)

@pytest.mark.parametrize('name, description, expected_name, expected_desc', test_param)
def test_contenttype_model(name, description, expected_name, expected_desc):
  data = ContentType(name=name, description=description)

  assert data.name == expected_name
  assert data.description == expected_desc

contentTypeList = [
  ContentType(name = "name1", description="desc1"),
  ContentType(name = "name2", description="desc2"),
  ContentType(name = "name3", description="desc3")
]

cat_test_param = (
  ["catname1","catdescp1",contentTypeList[0], "catname1", "catdescp1",contentTypeList[0]],
  ["catname2","catdescp2",contentTypeList[1], "catname2", "catdescp2",contentTypeList[1]],
  ["catname3","catdescp3",contentTypeList[2], "catname3", "catdescp3",contentTypeList[2]]
)

@pytest.mark.parametrize('name, description, type, expected_name, expected_desc, expected_type', cat_test_param)
def test_catagory_model(name, description, type, expected_name, expected_desc, expected_type):
  data = Category(name=name, description=description, content_type=type)

  assert data.name == expected_name
  assert data.description == expected_desc
  assert data.content_type == expected_type