
import os
import time
import glob

from datetime import datetime

from loghandler import Log



#returns the last created log file inside the given directory
def get_newer_log(logs_path:str) -> str:
    list_of_logs = glob.glob(logs_path)
    return max(list_of_logs, key=os.path.getmtime)



#returns the last modified date of the log file
def get_log_mdate(log_path:str) -> datetime:
    log_str_mdate = time.ctime(os.path.getmtime(log_path))
    log_mdate = datetime.strptime(log_str_mdate, '%a %b %d %H:%M:%S %Y')
    log_mdate.strftime("%m/%d/%Y")
    return log_mdate


#returns true if device under test log exists
def dut_log_exists(logs_path:str, ref_date:datetime) -> bool:
    log_paths = glob.glob(logs_path)
    for log_path in log_paths:
        log_mdate = get_log_mdate(log_path)
        if log_mdate > ref_date:
            return True
    return False

def get_all_test_names(log:Log) -> list:
    test_names = []
    with open(log.path) as log_file:
        lines = log_file.readlines()
        passed_lines = []
        for line in lines:
            passed_lines.append(line)
            if 'FAIL' in line or 'PASS' in line:
                test_info = log.get_test_info(passed_lines, readable=True)
                count_result = sum(test_info in s for s in test_names) + 1
                if count_result > 1:
                    test_names.append(test_info + "-" + str(count_result))
                else:
                    test_names.append(test_info + "-1")
    return test_names


def get_all_limits(log:Log, edge_side:str) -> list:
    limits = []
    with open(log.path) as log_file:
        lines = log_file.readlines()
        for line in lines:
            if 'FAIL' in line or 'PASS' in line:
                limit = log.get_result_info(line)[edge_side + " limit"]
                limits.append(limit)
    return limits



    

