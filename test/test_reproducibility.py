# TODO: Configured reproducibility tests that can be run to test each stage of model development.
import filecmp
import logging
import os
import subprocess

import json
import yaml

dict_file_types = ["json", "yml", "yaml"]

logger = logging.getLogger(__name__)


def run_tests(args=None, config_path=None):
    """Runs commands in config file and compares the generated files to those that are expected."""

    if args is not None:
        config_path = args.config

    with open(config_path, "r") as f:
        tests = yaml.load(f, Loader=yaml.FullLoader)

    all_passed = True
    for test in tests:
        testconf = tests[test]
        subprocess.check_output(testconf["command"].split())

        true_dir, test_dir = testconf["true_dir"], testconf["test_dir"]

        files_to_compare = [f for f in testconf["files_to_compare"] if f.split('.')[-1] not in dict_file_types]
        match, mismatch, errors = filecmp.cmpfiles(true_dir, test_dir, files_to_compare, shallow=True)

        if len(mismatch) > 0:
            logger.warning("%s file(s) does not match, %s test FAILED" % (", ".join(mismatch), test))
            all_passed = False
        else:
            logger.warning("%s test PASSED" % test)

    if all_passed:
        logger.warning("Success, all test passed!")