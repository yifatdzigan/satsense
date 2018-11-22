"""Implementation of the NDXI family of features."""
from functools import partial

import numpy as np

from ..image import Image
from .feature import Feature

NDXI_TYPES = {
    'nir_ndvi': ('red', 'nir-1'),
    'rg_ndvi': ('red', 'green'),
    'rb_ndvi': ('red', 'blue'),
    'ndsi': ('green', 'nir-1'),
    'ndwi': ('coastal', 'nir-2'),
    'wvsi': ('green', 'yellow'),
}


def ndxi_image(image: Image, ndxi_type):
    """Calculates the feature according to the ndxi option provided."""
    band_0_name, band_1_name = NDXI_TYPES[ndxi_type]
    band_0 = image[band_0_name]
    band_1 = image[band_1_name]

    band_mix = band_0 + band_1
    # Ignore divide, this division may complain about division by 0
    # This usually happens in the edge, which is alright by us.
    old_settings = np.seterr(divide='ignore', invalid='ignore')
    ndxi = np.divide(band_0 - band_1, band_mix)
    ndxi[band_mix == 0] = 0
    np.seterr(**old_settings)

    return ndxi


for itype in NDXI_TYPES:
    Image.register(itype, partial(ndxi_image, ndxi_type=itype))


def print_ndxi_statistics(ndxi, option):
    """Prints the ndvi matrix and the, min, max, mean and median."""
    print('{o} matrix: '.format(o=option))
    print(ndxi)

    print('\nMax {o}: {m}'.format(o=option, m=np.nanmax(ndxi)))
    print('Mean {o}: {m}'.format(o=option, m=np.nanmean(ndxi)))
    print('Median {o}: {m}'.format(o=option, m=np.nanmedian(ndxi)))
    print('Min {o}: {m}'.format(o=option, m=np.nanmin(ndxi)))


class NDXI(Feature):
    """The parent class of the family of NDXI features."""
    size = 1
    compute = staticmethod(np.mean)


class NirNDVI(NDXI):
    """The infrared-green normalized difference vegetation index of the image."""
    base_image = 'nir_ndvi'


class RgNDVI(NDXI):
    """The red-green normalized difference vegetation index of the image."""
    base_image = 'rg_ndvi'


class RbNDVI(NDXI):
    """The red-blue normalized difference vegetation index of the image."""
    base_image = 'rb_ndvi'


class NDSI(NDXI):
    """The snow cover index of the image."""
    base_image = 'ndsi'


class NDWI(NDXI):
    """The water cover index of the image."""
    base_image = 'ndwi'


class WVSI(NDXI):
    """The soil cover index of the image."""
    base_image = 'wvsi'
