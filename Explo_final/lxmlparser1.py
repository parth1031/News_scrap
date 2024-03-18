from lxml import html
import requests



class HTMLParser:
    def __init__(self, html_content):
        self.tree = html.fromstring(html_content)

    def get_text_by_tag(self, tag_name=None, attribute_name=None, attribute_value=None):
        if tag_name and attribute_name and attribute_value:
            xpath_query = f'//{tag_name}[@{attribute_name}="{attribute_value}"]'
        elif not tag_name and attribute_name and attribute_value:
        
            xpath_query = f'//*[@{attribute_name}="{attribute_value}"]'
        else:
            xpath_query = f'//{tag_name}'
    
        elements = self.tree.xpath(xpath_query)
    
        result_list = []
        for element in elements:
            result_list.append(element.text_content().strip())
    
        return result_list


    
    def parent(self, tag_name=None, attribute_name=None, attribute_value=None):
        result_list = []
    
        if tag_name and attribute_name and attribute_value:
            xpath_query = f'//{tag_name}[@{attribute_name}="{attribute_value}"]'
        elif not tag_name and attribute_name and attribute_value:
            xpath_query = f'//*[@{attribute_name}="{attribute_value}"]'
        else:
            xpath_query = f'//{tag_name}'
    
        elements = self.tree.xpath(xpath_query)
        parents=[]
        
    
        for element in elements:
            parent = element.getparent()
            parents.append(parent)
        return parents


    def children(self, tag_name=None, attribute_name=None, attribute_value=None):
        result_list = []
        if tag_name and attribute_name and attribute_value:
            xpath_query = f'//{tag_name}[@{attribute_name}="{attribute_value}"]'
        elif not tag_name and attribute_name and attribute_value:
            xpath_query = f'//*[@{attribute_name}="{attribute_value}"]'
        else:
            xpath_query = f'//{tag_name}'
        
        elements = self.tree.xpath(xpath_query)
        for element in elements:
            parent = element.getparent()
            if parent is not None:
                result_dict = {'tag': parent.tag, 'attributes': {}}
                    
                    
                for key, value in parent.items():
                    result_dict['attributes'][key] = value
                    
                result_list.append(result_dict)
        
        return result_list
    
    def find_all_next(self, tag_name=None, attribute_name=None, attribute_value=None):
        result_list = []

        if tag_name and attribute_name and attribute_value:
            xpath_query = f'//{tag_name}[@{attribute_name}="{attribute_value}"]/following-sibling::*'
        elif not tag_name and attribute_name and attribute_value:
            xpath_query = f'//*[@{attribute_name}="{attribute_value}"]/following-sibling::*'
        elif tag_name:
            xpath_query = f'//{tag_name}/following-sibling::*'
        else:
        # Handle the case where neither tag_name nor attribute_name and attribute_value are provided
            return result_list

        elements = self.tree.xpath(xpath_query)

        for element in elements:
            result_dict = {'tag': element.tag,  'attributes': {}}

            # Append attributes and their values to the result_dict
            for key, value in element.items():
                result_dict['attributes'][key] = value

            result_list.append(result_dict)

        return result_list


    def find_all_tags(self, tag_name):
        result_list = []

        elements = self.tree.xpath(f'//{tag_name}')

        for element in elements:
            result_dict = {'tag': element.tag, 'attributes': {}}

            # Append attributes and their values to the result_dict
            for key, value in element.items():
                result_dict['attributes'][key] = value

            result_list.append(result_dict)

        return result_list


    def find_all_by_attribute(self, attribute_name=None, attribute_value=None):
        result_list = []

        if attribute_name and attribute_value:
            xpath_query = f'//*[@{attribute_name}="{attribute_value}"]'
        elif attribute_name:
            xpath_query = f'//*[@{attribute_name}]'
        elif attribute_value:
            xpath_query = f'//*[@*="{attribute_value}"]'
        else:
            # Handle the case where neither attribute_name nor attribute_value is provided
            return result_list
    
        elements = self.tree.xpath(xpath_query)
    
        for element in elements:
            result_dict = {'tag': element.tag, 'attributes': {}}
    
            # Append attributes and their values to the result_dict
            for key, value in element.items():
                result_dict['attributes'][key] = value
    
            result_list.append(result_dict)
    
        return result_list



