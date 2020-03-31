import unittest
import logging
import logging.config

from pathlib import Path
from flask_testing import TestCase
from click.testing import CliRunner
from src.caps import __main__

logging_file = Path(__file__).parent.parent / "settings" / "logging.ini"
try:
    logging.config.fileConfig(logging_file)
except:
    logging.error("Logging config file does not exist {}".format(logging_file))
    exit(0)
logger = logging.getLogger(__name__)

class TestCapsCliCommands(unittest.TestCase):
    def test_configure_command(self):
        runner = CliRunner()
        result = runner.invoke(__main__.configure, ['--profile', 'test_profile'], input="mlsnfklsd\nkjahdkasj")
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()