import json
import string
from awscli.customizations.cloudformation.yamlhelper import yaml_parse


class CfnTemplate(string.Template):
    delimiter = '$'
    idpattern = r'[a-z][\w\,\+\=\:\-\.\x2f\x5c\*\(\)\[\]\x7c]*'


class DynamoDBResource:
    def __init__(self, resource):
        self.resource = resource

    def tableName(self):
        return self.resource['Properties']['TableName']

    def properties(self):
        return self.resource['Properties']


class CFNParser:

    # not supported in dynamodb-local
    EXCLUDED_PROPERTIES = ['TimeToLiveSpecification']

    def __init__(self, filename, parameters):
        self.parameters = parameters
        self.template = self.__load_yaml(filename)
        self.resources = self.template['Resources']

    def all_dynamodb_tables(self):
        for key in self.resources.keys():
            resource = self.resources[key]
            if resource['Type'] == 'AWS::DynamoDB::Table':
                self.__remove_unsupported_properties(resource)
                self.__resolve_parameters(resource)
                yield DynamoDBResource(resource)

    def __load_yaml(self, filename):
        with open(filename) as f:
            return yaml_parse(f.read())

    def __remove_unsupported_properties(self, node):
        if isinstance(node['Properties'], dict):
            for key in self.EXCLUDED_PROPERTIES:
                if key in node['Properties']:
                    del node['Properties'][key]

    def __resolve_parameters(self, node):
        for key in node:
            val = node[key]
            if isinstance(val, dict):
                if len(val) == 1:
                    nextkey = next(iter(val))
                    if nextkey.startswith('Fn::'):
                        if nextkey == 'Fn::Sub':
                            node[key] = CfnTemplate(
                                val['Fn::Sub']).safe_substitute(self.parameters)
                        else:
                            print(f"{nextkey} skipped")
                            del node[key]

                self.__resolve_parameters(val)
