from unittest import TestLoader, TestSuite, TextTestRunner
from _01_alerts import AlertsTest
from _01_alerts_dismiss import AlertsDismissTest
from _01_alerts_input import AlertsInputTest

alerts = TestLoader().loadTestsFromTestCase(AlertsTest)
alerts_dismiss =  TestLoader().loadTestsFromTestCase(AlertsDismissTest)
alerts_input =  TestLoader().loadTestsFromTestCase(AlertsInputTest)

suite = TestSuite([alerts,alerts_dismiss,alerts_input])


# Run tests
if __name__ == "__main__":
    runner = TextTestRunner(verbosity=2)  # verbosity=2 for detailed output
    runner.run(suite)