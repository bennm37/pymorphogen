from hcrp.labelling import get_spline, get_contour
import numpy as np
from skimage.io import imread

dropbox_root = "/Users/huanga/The Francis Crick Dropbox/VincentJ/Anqi/Intership/AI_segmentation/python_segmentation/"
filename = "TdEmbryo_Hoechst_pMad488_dpp546_brk647_20240506_LimbExtension10-Ant"
def test_get_spline():
    stack = np.array(imread(f'{dropbox_root}{filename}.tif'))
    layer = 26
    img = stack[layer, :, :, 3]
    get_spline(img, f'{filename}')

def test_get_contour():
    stack = np.array(imread(f'{dropbox_root}{filename}.tif'))
    layer = 26
    img = stack[layer, :, :, 3]
    get_contour(img, f'{filename}')


if __name__ == '__main__':
    test_get_spline()
    test_get_contour()