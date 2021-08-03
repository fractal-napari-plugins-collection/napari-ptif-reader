"""
Unittests for napri_ptif_reader.napari_ptif_reader module.
"""
import numpy as np
from types import SimpleNamespace

from napari_ptif_reader.napari_ptif_reader import ptif_reader


def test_ptif_reader(mocker):
    """
    Test for the napari_ptifreader.ptif_reader() function.
    """
    def mock_tifffile_init(self, image_path):
        self.data = [
            np.ones((16, 16)),
            np.ones((8, 8)),
            np.ones((4, 4)),
            np.ones((2, 2))
        ]
        return None
    def mock_tifffile_read_subfile_region(
        self, zoom, x1_pos, y1_pos, x2_pos, y2_pos
    ):
        return self.data[zoom][y1_pos:y2_pos, x1_pos:x2_pos]

    mocker.patch(
        'pylibtiff.TiffFile.__init__', mock_tifffile_init
    )
    mocker.patch(
        'pylibtiff.TiffFile.subfile_tags',
        new_callable=mocker.PropertyMock,
        return_value=[
            SimpleNamespace(**{
                'image_length': 16, 'image_width': 16,
                'tile_length': 4, 'tile_width': 4
            }),
            SimpleNamespace(**{
                'image_length': 8, 'image_width': 8,
            }),
            SimpleNamespace(**{
                'image_length': 4, 'image_width': 4,
            }),
            SimpleNamespace(**{
                'image_length': 2, 'image_width': 2,
            })
        ]
    )
    mocker.patch(
        'pylibtiff.TiffFile.read_subfile_region', mock_tifffile_read_subfile_region
    )

    layer_data = ptif_reader(...)
    print(layer_data)
    assert len(layer_data) == 1
    pyramid, _ = layer_data[0]
    assert len(pyramid) == 3
    lvl0_array = pyramid[0]
    assert lvl0_array.shape == (16, 16)
    assert lvl0_array.sum().compute() == 16 * 16
