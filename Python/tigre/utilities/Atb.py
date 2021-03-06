from _Atb import _Atb_ext
import numpy as np
import copy
from .gpu import GpuIds

def Atb(projections, geo, angles,  krylov="matched", **kwargs):

    if projections.dtype != np.float32:
        raise TypeError("Input data should be float32, not " + str(projections.dtype))
    if not np.isreal(projections).all():
        raise ValueError("Complex types not compatible for back projection.")
    geox = copy.deepcopy(geo)
    geox.check_geo(angles)
    """
       Here we cast all values in geo to single point precision float. This way we 
       know what behaviour to expect from pytigre to Cuda and can change 
       single parameters accordingly. 
    """
    geox.cast_to_single()
    #geox.checknans()

    if projections.shape != (geox.angles.shape[0],geox.nDetector[0],geox.nDetector[1]):
        raise ValueError("Expected data shape: " + str((geox.angles.shape[0], geox.nDetector[0],geox.nDetector[1])) +
                         " not compatible with: " + str(projections.shape))

    if not 'gpuids' in kwargs or kwargs['gpuids'] is None:
        gpuids = GpuIds()
    else:
        gpuids = kwargs['gpuids']

    return _Atb_ext(projections, geox, geox.angles, krylov,geox.mode, gpuids=gpuids)
    