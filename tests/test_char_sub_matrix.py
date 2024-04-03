import unittest

import numpy as np

from line_align.pylib import char_sub_matrix


class TestCharSubMatrix(unittest.TestCase):
    def test_get_max_iou_01(self):
        pix1 = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )
        pix2 = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )
        self.assertEqual(char_sub_matrix.get_max_iou(pix1, pix2), 1.0)

    def test_get_max_iou_02(self):
        pix1 = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 1.0],
                [0.0, 0.0, 0.0],
            ]
        )
        pix2 = np.array(
            [
                [1.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )
        self.assertEqual(char_sub_matrix.get_max_iou(pix1, pix2), 1.0)

    def test_get_max_iou_03(self):
        pix1 = np.array(
            [
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        )
        pix2 = np.array(
            [
                [1.0, 1.0, 1.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )
        self.assertEqual(char_sub_matrix.get_max_iou(pix1, pix2), 0.2)
