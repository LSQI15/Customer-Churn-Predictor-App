import filecmp
import logging
import subprocess
import yaml

dict_file_types = ["json", "yml", "yaml"]
logger = logging.getLogger(__name__)


def run_reproducibility_tests(args=None, config_path=None):
    """Runs commands in config file and compares the generated files to those that are expected."""

    if args is not None:
        config_path = args.config

    with open(config_path, "r") as f:
        tests = yaml.load(f, Loader=yaml.FullLoader)

    all_passed = True
    for test in tests:
        # log the test configurations
        testconf = tests[test]
        # compare whether csv files generated by the model pipeline is the same as the expected files
        # located in test/true folder
        true_dir, test_dir = testconf["true_dir"], testconf["test_dir"]
        files_to_compare = [f for f in testconf["files_to_compare"] if f.split('.')[-1] not in dict_file_types]
        match, mismatch, errors = filecmp.cmpfiles(true_dir, test_dir, files_to_compare, shallow=True)

        if len(mismatch) > 0:
            logger.warning("%s file(s) does not match, reproducibility test of model pipeline step \'%s\': FAILED" % (
            ", ".join(mismatch), test))
            all_passed = False
        else:
            logger.info("Reproducibility test of model pipeline stage \'%s\': PASSED" % test)

    if all_passed:
        logger.info("Success, all reproducibility tests passed!")
