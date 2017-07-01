import unittest
from HexStringConverter import parseHexString, convertEncoderData, convertRawCountsDistance,convertRawCountsForce, convertOneFile


class TestStringMethods(unittest.TestCase):

    def test_parseHexString(self):

        self.assertListEqual(parseHexString("a", 1), [10])
        self.assertListEqual(parseHexString("aa", 2), [170])
        self.assertListEqual(parseHexString("208b208f209a2085", 4), [8331, 8335, 8346, 8325])


    def test_convertRawCountsDistance(self):

        self.assertListEqual(convertRawCountsDistance([0, 10000, 20000, 30000, 45000, 62830]), [0, 1, 2, 3, 4.5, 6.283])
        self.assertEqual(convertRawCountsDistance([]), [])

    def test_convertRawCountsForce(self):

        self.assertEqual(convertRawCountsForce([]), [])
        self.assertListEqual(convertRawCountsForce([0, 10000, 20000, 45000, 60000]),
                             [-1.475, -0.0283, 1.4184, 5.0351, 7.2052])

    def test_convertEncoderData(self):
        """Testing the Encoder conversion is tricky, because it depends so much on the tuning of the values that the
        algorithm is using. If a better method can be found for converting encoder data, better tests should be
        formulated as well. UPDATE: If we take advantage of the Index channel on the encoder the program will no
        longer have to guess when rollover has occurred because that will be tracked by the encoder. """
        self. assertListEqual(convertEncoderData("000001f4271048440064177046502710138800c8"),
                              [0, 500, 10000, 18500, 20100, 26000, 18000, 10000, 5000, 200])

    def test_convertOneFile(self):
        """Better testing of this function would also be nice, but I was too lazy to write it because the
        input files are really long"""
        self.assertEqual(convertOneFile(['C:/Users/TestFile.log', ['ForceDataHex: ', "aaaa"], ['PosDataHex: ', "aaaa"]]).Force
                         , [[-1.4504]])

        self.assertEqual(convertOneFile(['C:/Users/TestFile.log', ['ForceDataHex: ', "aaaa"], ['PosDataHex: ', "aaaa"]]).Pos
                         , [[.017]])

        self.assertEqual(convertOneFile(['C:\Users/TestFile.log', ['ForceDataHex: ', "aaaa"], ['PosDataHex: ', "aaaa"]]).Name
                         , 'TestFile.log')

if __name__ == '__main__':
    unittest.main()
