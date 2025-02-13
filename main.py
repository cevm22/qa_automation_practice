from unittest import TestLoader, TestSuite, TextTestRunner
from _01_alerts import AlertsTest
from _01_alerts_dismiss import AlertsDismissTest

alerts = TestLoader().loadTestsFromTestCase(AlertsTest)
alerts_dismiss =  TestLoader().loadTestsFromTestCase(AlertsDismissTest)

suite = TestSuite([alerts,alerts_dismiss])


# Run tests
if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)  # verbosity=2 for detailed output
    runner.run(suite)