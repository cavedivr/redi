import json
import unittest
import tempfile
import os
import sys

from lxml import etree
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
import redi

class TestUpdateDataFromLookup(unittest.TestCase):

    def setUp(self):
        self.raw_xml = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>03/08/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>03/08/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/07/19</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName/></subject>
</study>
"""
        self.data_tree = etree.ElementTree(etree.fromstring(self.raw_xml))

        self.form_events = """<?xml version='1.0' encoding='US-ASCII'?>
<redcapProject>
	<name>My Test Project</name>
	<form>
		<name>cbc</name>
		<formDateField>cbc_lbdtc</formDateField>
		<formCompletedFieldName>cbc_complete</formCompletedFieldName>
		<event>
			<name>1_arm_1</name>
		</event>
		<event>
			<name>2_arm_1</name>
		</event>
		<event>
			<name>3_arm_1</name>
		</event>
    </form>
	<form>
		<name>chemistry</name>
		<formDateField>chemistry_lbdtc</formDateField>
		<formCompletedFieldName>chemistry_complete</formCompletedFieldName>
		<event>
			<name>1_arm_1</name>
		</event>
		<event>
			<name>2_arm_1</name>
		</event>
		<event>
			<name>3_arm_1</name>
		</event>
    </form>
</redcapProject>
"""


        self.form_events_tree = etree.ElementTree(etree.fromstring(self.form_events))

        self.output = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>03/08/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMATOCRIT</Component_Name>
        <Component_ID>1534436</Component_ID>
        <Reference_Unit>%</Reference_Unit>
        <Result_Value>34.5</Result_Value>
    <timestamp/><redcapFormName>undefined</redcapFormName><eventName/><formDateField/><formCompletedFieldName>undefined</formCompletedFieldName></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>03/08/19</Collection_Date>
        <Collection_Time>13:50</Collection_Time>
        <Component_Name>HEMOGLOBIN</Component_Name>
        <Component_ID>1534435</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Result_Value>11.3</Result_Value>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField/><formCompletedFieldName>cbc_complete</formCompletedFieldName></subject>
    <subject>
        <Study_Id>22</Study_Id>
        <Collection_Date>10/07/19</Collection_Date>
        <Collection_Time>12:38</Collection_Time>
        <Component_Name>BILIRUBIN DIRECT</Component_Name>
        <Component_ID>1558221</Component_ID>
        <Reference_Unit>mg/dL</Reference_Unit>
        <Result_Value>0.8</Result_Value>
    <timestamp/><redcapFormName>chemistry</redcapFormName><eventName/><formDateField/><formCompletedFieldName>chemistry_complete</formCompletedFieldName></subject>
</study>
"""
        self.expect = etree.tostring(etree.fromstring(self.output))
        return()


    def test_update_data_from_lookup(self):
        element_to_set_in_data = 'formCompletedFieldName'
        index_element_in_data = 'redcapFormName'
        element_to_find_in_lookup_data = 'form'
        index_element_in_lookup_data = 'name'
        value_in_lookup_data = 'formCompletedFieldName'
        undefined = 'undefined'

        redi.update_data_from_lookup(self.data_tree, element_to_set_in_data, index_element_in_data, self.form_events_tree, element_to_find_in_lookup_data, index_element_in_lookup_data, value_in_lookup_data, undefined)

        self.result = etree.tostring(self.data_tree)
        self.assertEqual(self.expect, self.result)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
