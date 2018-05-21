import ROOT
import subprocess

path_to_fcl_config = "fragment_to_digit.fcl"

# map the input file location to the output file location
def digits_file_name(fragments_file_name):
    return fragments_file_name.replace(".root", "_digits.root")

# given the path to a fragments file, gnerates an art root file
def process(fragments_file_loc):
    digit_file_loc = digits_file_name(fragments_file_loc)

    # setup command
    command = ["lar", "-c", path_to_fcl_config, "-s", fragments_file_loc, "-T", digit_file_loc]

    try:
        # try to run latsoft
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        code = 0
    except subprocess.CalledProcessError, err:
        # if it fails, still get info
        output = err.output 
        code = err.returncode
    return (code, output)

