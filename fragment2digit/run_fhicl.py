import os
import subprocess

# given the path to a fragments file, gnerates an art root file
def process(fragments_file_loc, fhicl_configs):
    ret = []
    for fhicl in fhicl_configs:
        command_ret = process_command(fragments_file_loc, fhicl)
        ret.append(command_ret)
    return ret

def process_command(fragments_file_loc, path_to_fcl_config):
    # setup command
    command = ["lar", "-c", path_to_fcl_config, "-s", fragments_file_loc]
    # TEST command
    # command = ["cp", fragments_file_loc, digit_file_loc]

    try:
        # try to run latsoft
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        code = 0
    except subprocess.CalledProcessError, err:
        # if it fails, still get info
        output = err.output 
        code = err.returncode
    return (code, output)

