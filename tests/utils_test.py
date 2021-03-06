import unittest
import struct

from zttf.utils import fixed_version, binary_search_parameters, ttf_checksum, glyph_more_components, glyf_skip_format


class TestUtils(unittest.TestCase):
    def test_fixed_version(self):
        cases = [
            (0x00005000, 0.5),
            (0x00010000, 1.0),
            (0x00035000, 3.5),
            (0x00105000, 10.5)
        ]
        for case in cases:
            self.assertEqual(fixed_version(case[0]), case[1])

    def test_binary_parameters(self):
        cases = {
            39: (32, 5),
            10: (8, 3),
            19: (16, 4)
        }
        for n, result in cases.items():
            self.assertEqual(binary_search_parameters(n), result)

    def test_checksum(self):
        data = struct.pack(">12I", *range(0, 12))
        self.assertEqual(len(data), 48)
        self.assertEqual(ttf_checksum(data), 66)
        self.assertEqual(ttf_checksum(struct.pack(">12I", *range(1000, 13000, 1000))), 78000)
        self.assertEqual(ttf_checksum(struct.pack(">512I", *range(1024, 1024 * 2048, 4096))), 0x1FF80000)

    def test_component_flag(self):
        self.assertTrue(glyph_more_components((1 << 5)))
        self.assertFalse(glyph_more_components((1 << 4)))

    def test_skip_format(self):
        self.assertEqual(glyf_skip_format((1 << 0)), ">I")
        self.assertEqual(glyf_skip_format(0), ">H")
        self.assertEqual(glyf_skip_format((1 << 3)), ">HH")
        self.assertEqual(glyf_skip_format((1 << 3) | (1 << 0)), ">IH")
        self.assertEqual(glyf_skip_format((1 << 7)), ">HII")

