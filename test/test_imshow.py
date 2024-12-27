import sys
sys.path.append('.')
import skrbcr_casa_scripts as my


def test_lazy_raster(show=False):
    my.lazy_raster('test/twhya_cont.image', show=show)


if __name__ == '__main__':
    test_lazy_raster(show=True)
