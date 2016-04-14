# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ....testing import assert_equal
from ..utils import SmoothTessellation


def test_SmoothTessellation_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    curvature_averaging_iterations=dict(argstr='-a %d',
    ),
    disable_estimates=dict(argstr='-nw',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    gaussian_curvature_norm_steps=dict(argstr='%d ',
    ),
    gaussian_curvature_smoothing_steps=dict(argstr='%d',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='%s',
    copyfile=True,
    mandatory=True,
    position=-2,
    ),
    normalize_area=dict(argstr='-area',
    ),
    out_area_file=dict(argstr='-b %s',
    ),
    out_curvature_file=dict(argstr='-c %s',
    ),
    out_file=dict(argstr='%s',
    genfile=True,
    position=-1,
    ),
    seed=dict(argstr='-seed %d',
    mandatory=False,
    ),
    smoothing_iterations=dict(argstr='-n %d',
    ),
    snapshot_writing_iterations=dict(argstr='-w %d',
    ),
    subjects_dir=dict(),
    terminal_output=dict(nohash=True,
    ),
    use_gaussian_curvature_smoothing=dict(argstr='-g',
    ),
    use_momentum=dict(argstr='-m',
    ),
    )
    inputs = SmoothTessellation.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(inputs.traits()[key], metakey), value


def test_SmoothTessellation_outputs():
    output_map = dict(surface=dict(),
    )
    outputs = SmoothTessellation.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(outputs.traits()[key], metakey), value
