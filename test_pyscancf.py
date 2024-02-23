import unittest


class TestPyScanCf(unittest.TestCase):
    def test_version(self):
        import pyscancf

        self.assertEqual(pyscancf.__version__, "1.0.29")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestPyScanCf("test_version"))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
