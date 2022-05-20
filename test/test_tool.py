import sys,os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospwork.tool import get_base_web_data,get_work_page

def test_base_soup():
   test = get_base_web_data("https://www.google.com")
   assert 'Google' in test.text

def test_workpage_soup():
   test = get_work_page("https://www.google.com")
   assert 'Google' in test.text
