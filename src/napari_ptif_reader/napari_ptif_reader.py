"""
Main module containing the reader for multi-scale (pyramidal) TIFF files.
"""
import dask.array as da
import dask
from napari_plugin_engine import napari_hook_implementation
import numpy as np
from pylibtiff import TiffFile


def ptif_reader(path):
    """
    Function which reads a multi-scale (pyramidal) TIFF file as delayed Dask
    array.

    :param path: The path of the image
    :return: List of LayerData tuple
    """
    @dask.delayed
    def read_tile(image_path, x_pos, y_pos, z_pos, width, height):
        # pylint: disable=R0913
        """
        Function which reads a region from a .ptif file as a Numpy array.

        :param image_path: The path to the .ptif file
        :param x_pos: The x position of the region
        :param y_pos: The y position of the region
        :param z_pos: The zoom level of the region
        :param width: The width of the region
        :param height: The height of the region
        :return: The Numpy array
        """
        ptif = TiffFile(image_path)
        data = np.zeros([height, width], dtype=np.uint8)
        data[:height, :width] = ptif.read_subfile_region(
            z_pos, x_pos, y_pos, x_pos+width, y_pos+height
        )
        return data

    ptif = TiffFile(path)
    assert ptif.subfile_tags[0].tile_length == ptif.subfile_tags[0].tile_width

    tile_size = ptif.subfile_tags[0].tile_width

    pyramid = []
    for page in range(len(ptif.subfile_tags)):
        if ptif.subfile_tags[page].image_width < tile_size:
            break

        dask_arrays = []
        y_tiles = ptif.subfile_tags[page].image_length // tile_size + 1
        x_tiles = ptif.subfile_tags[page].image_width // tile_size + 1
        for y_tile in range(y_tiles):
            tile_height = min(
                ptif.subfile_tags[page].image_length - y_tile * tile_size, tile_size
            )
            row_tiles = []
            for x_tile in range(x_tiles):
                tile_width = min(
                    ptif.subfile_tags[page].image_width - x_tile * tile_size, tile_size
                )
                row_tiles.append(
                    da.from_delayed(
                        read_tile(
                            path, x_tile*tile_size, y_tile*tile_size, page, tile_width, tile_height
                        ),
                        shape=(tile_height, tile_width), dtype=np.uint8
                    )
                )
            dask_arrays.append(row_tiles)

        pyramid.append(da.block(dask_arrays))

    kwargs = {}
    return [(pyramid, kwargs)]


@napari_hook_implementation
def napari_get_reader(path):
    """
    Napari plugin that returns a reader for .ptif images.

    .. note::
       This hook does not support a list of paths

    :param path:  The path of the image
    :return: The ptif_reader function or None
    """
    if isinstance(path, str) and path.endswith(".ptif"):
        return ptif_reader
    return None
