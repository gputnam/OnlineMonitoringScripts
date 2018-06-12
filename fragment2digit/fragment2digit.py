import os
import subprocess

path_to_fcl_config = "/home/nfs/sbnddqm/SBND_DAQ/online_analysis/srcs/sbndcode/sbndcode/VSTAnalysis/fcl/DAQ/digits.fcl"

path_to_digits_out = "/home/nfs/sbnddqm/SBND_DAQ/test_fragment_to_digit/digit/"

# map the input file location to the output file location
def digits_file_name(fragments_file_path):
    # get the file name
    _, fragments_file_name = os.path.split(fragments_file_path)
    return path_to_digits_out + "digits_" + fragments_file_name

# given the path to a fragments file, gnerates an art root file
def process(fragments_file_loc):
    digit_file_loc = digits_file_name(fragments_file_loc)

    # setup command
    command = ["lar", "-c", path_to_fcl_config, "-s", fragments_file_loc, "-T", digit_file_loc]
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

