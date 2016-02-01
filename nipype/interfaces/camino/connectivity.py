"""
    Change directory to provide relative paths for doctests
    >>> import os
    >>> filepath = os.path.dirname( os.path.realpath( __file__ ) )
    >>> datadir = os.path.realpath(os.path.join(filepath, '../../testing/data'))
    >>> os.chdir(datadir)

"""
import os

from ..base import (traits, TraitedSpec, File,
                    CommandLine, CommandLineInputSpec, isdefined)
from ...utils.filemanip import split_filename


class ConmatInputSpec(CommandLineInputSpec):
    in_file = File(exists=True, argstr='-inputfile %s', mandatory=True,
                   desc='Streamlines as generated by the Track interface')

    target_file = File(exists=True, argstr='-targetfile %s', mandatory=True,
                       desc='An image containing targets, as used in ProcStreamlines interface.')

    scalar_file = File(exists=True, argstr='-scalarfile %s',
                       desc=('Optional scalar file for computing tract-based statistics. '
                             'Must be in the same space as the target file.'),
                       requires=['tract_stat'])

    targetname_file = File(exists=True, argstr='-targetnamefile %s',
                           desc=('Optional names of targets. This file should contain one entry per line, '
                                 'with the target intensity followed by the name, separated by white space. '
                                 'For example: '
                                 '  1  some_brain_region '
                                 '  2     some_other_region '
                                 'These names will be used in the output. The names themselves should not '
                                 'contain spaces or commas. The labels may be in any order but the output '
                                 'matrices will be ordered by label intensity.'))

    tract_stat = traits.Enum("mean", "min", "max", "sum", "median", "var", argstr='-tractstat %s', units='NA',
                             desc=("Tract statistic to use. See TractStats for other options."),
                             requires=['scalar_file'], xor=['tract_prop'])

    tract_prop = traits.Enum("length", "endpointsep", argstr='-tractstat %s',
                             units='NA', xor=['tract_stat'],
                             desc=('Tract property average to compute in the connectivity matrix. '
                                   'See TractStats for details.'))

    output_root = File(argstr='-outputroot %s', genfile=True,
                       desc=('filename root prepended onto the names of the output files. '
                             'The extension will be determined from the input.'))


class ConmatOutputSpec(TraitedSpec):
    conmat_sc = File(exists=True, desc='Connectivity matrix in CSV file.')
    conmat_ts = File(desc='Tract statistics in CSV file.')


class Conmat(CommandLine):
    """
    Creates  a  connectivity  matrix  using a 3D label image (the target image)
    and a set of streamlines. The connectivity matrix records how many stream-
    lines connect each pair of targets, and optionally the mean tractwise
    statistic (eg tract-averaged FA, or length).

    The output is a comma separated variable file or files. The first row of
    the output matrix is label names. Label names may be defined by the user,
    otherwise  they  are assigned based on label intensity.

    Starting  from the seed point, we move along the streamline until we find
    a point in a labeled region. This is done in both directions from the seed
    point. Streamlines are counted if they connect two target regions, one on
    either side of the seed point. Only the labeled region closest to the seed
    is counted, for example if the  input contains two streamlines: ::

         1: A-----B------SEED---C
         2: A--------SEED-----------

    then the output would be ::

         A,B,C
         0,0,0
         0,0,1
         0,1,0

    There  are  zero  connections  to A because in streamline 1, the connection
    to B is closer to the seed than the connection to A, and in streamline 2
    there is no region reached in the other direction.

    The connected target regions can have the same label, as long as the seed
    point is outside of the labeled region and both ends connect to the same
    label (which may  be in different locations). Therefore this is allowed: ::

         A------SEED-------A

    Such fibers will add to the diagonal elements of the matrix. To remove
    these entries, run procstreamlines with -endpointfile before running conmat.

    If the seed point is inside a labled region, it counts as one end of the
    connection.  So ::

         ----[SEED inside A]---------B

    counts as a connection between A and B, while ::

         C----[SEED inside A]---------B

    counts as a connection between A and C, because C is closer to the seed point.

    In all cases, distance to the seed point is defined along the streamline path.

    Example 1
    ---------
    To create a standard connectivity matrix based on streamline counts.

    >>> import nipype.interfaces.camino as cam
    >>> conmat = cam.Conmat()
    >>> conmat.inputs.in_file = 'tracts.Bdouble'
    >>> conmat.inputs.target_file = 'atlas.nii.gz'
    >>> conmat.run()        # doctest: +SKIP

    Example 1
    ---------
    To create a standard connectivity matrix and mean tractwise FA statistics.

    >>> import nipype.interfaces.camino as cam
    >>> conmat = cam.Conmat()
    >>> conmat.inputs.in_file = 'tracts.Bdouble'
    >>> conmat.inputs.target_file = 'atlas.nii.gz'
    >>> conmat.inputs.scalar_file = 'fa.nii.gz'
    >>> conmat.run()        # doctest: +SKIP
    """
    _cmd = 'conmat'
    input_spec = ConmatInputSpec
    output_spec = ConmatOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        output_root = self._gen_outputroot()
        outputs['conmat_sc'] = os.path.abspath(output_root + "sc.csv")
        outputs['conmat_ts'] = os.path.abspath(output_root + "ts.csv")
        return outputs

    def _gen_outfilename(self):
        return self._gen_outputroot()

    def _gen_outputroot(self):
        output_root = self.inputs.output_root
        if not isdefined(output_root):
            output_root = self._gen_filename('output_root')
        return output_root

    def _gen_filename(self, name):
        if name == 'output_root':
            _, filename, _ = split_filename(self.inputs.in_file)
            filename = filename + "_"
        return filename