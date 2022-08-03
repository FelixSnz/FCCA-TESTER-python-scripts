"""
This file contains the class "Batch" where a batch is consider a tests results container.

NOTE:the FCCA TESTER has 6 groups of tests, but the information of the group 4 is not
generated in the log files.

With that being said, this class defines a handler for the information contained 
in the logs generated by te FCCA TESTER
"""

#class that defines a log batch
class Batch():
    def __init__(self, batch_name, batch_info) -> None:
        self.name = batch_name
        self.info = batch_info
        self.temp_test = None
    
    #returns a list that contains all the tests
    #of the batch (each test is a python dictionary)
    def get_tests(self) -> list:
        return self.info["tests"]
    
    #returns a dictionary that contains the info
    #of the given test name
    def get_test_info(self, test_name:str) -> dict:
        for test in self.get_tests():
            if test["name"] == test_name:
                return test
    
    #reads the passed lines in reverse and returns the first ocurrance
    #of the test name for the batch 
    def search_test(self, passed_lines:list) -> dict:
        tests = self.get_tests()
        for line in reversed(passed_lines):
            if self.name in line:
                break
            for test in tests:
                if test["name"] in line:
                    self.temp_test = test
                    return test
        return None
    
    #reads the passed lines in reverse and returns the first ocurrance
    #of the sub tests for the passed test name
    def search_sub_test(self, test_name:str, passed_lines:list) -> str:
        sub_tests = self.temp_test["sub tests"]
        for line in reversed(passed_lines):
            if test_name in line:
                break
            for sub_test in sub_tests:
                if sub_test in line:
                    return sub_test
        return None
    
    #reads the passed lines in reverse and returns the first ocurrance
    #of the set values for the passed test name
    def search_test_set(self, test_name:str, passed_lines:str) -> str:
        test_sets = self.temp_test["SET"]
        for line in reversed(passed_lines):
            if test_name in line:
                break
            for test_set in test_sets:
                if test_set in line:
                    return test_set
        return None


