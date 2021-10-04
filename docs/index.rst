Pyramidal TIF Reader
-----------------------------------------

    Note: Reading fractions of an image (a.k.a. lazy loading) requires advanced data structures which Napari only supports recently. For a smooth user-experience it is recommended to activate the NAPARI_OCTREE flag **before** running Napari. You can do so from the command line **before** running napari.

    +----------------------------+----------------------------------------------------------------------------------------------------+
    | Windows                    | Linux/Mac                                                                                          |
    +============================+====================================================================================================+
    | .. code:: batch            | .. code:: shell                                                                                    |
    |                            |                                                                                                    |
    |    SET NAPARI_OCTREE=1     |    export NAPARI_OCTREE=1                                                                          |
    |    napari                  |    napari                                                                                          |
    |    SET NAPARI_OCTREE=0     |    export NAPARI_OCTREE=0                                                                          |
    +----------------------------+----------------------------------------------------------------------------------------------------+

    We recommend to create a batch/shell script with the above commands. Deactivating the octree feature at the end avoids conflicts when using Napari with non-multi-scale images later on.
    If you are not familiar with batch/shell scripts please refer to the following tutorials for `Windows <https://www.tutorialspoint.com/batch_script/batch_script_files.htm>`_ and `Linux/Mac <https://www.tutorialspoint.com/unix/shell_scripting.htm>`_.

Given you have a multi-scale (pyramidal) TIF file with a PTIF extension, you can simple drag-n-drop the image into Napari or open the file from within Napari via the "File/Open File(s)..." menu.

    Note: Fractal does not yet provide a tool to convert large-scale images into multi-scale images. For testing purposes, we recommend to install `ImageMagick <https://imagemagick.org/index.php>`_ and convert e.g. the test001.tif image into a test001.ptif image using the following command:

    .. code:: shell

       convert.exe test001.tif -define tiff:tile-geometry=1024x1024 -compress jpeg ptif:test001.ptif

    Please note as ImageMagick is a very powerful tool which allows you to specify many more options via the command line. For more details please refer to the `official reference <https://imagemagick.org/script/command-line-processing.php>`_.
