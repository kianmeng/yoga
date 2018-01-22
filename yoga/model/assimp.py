"""
This module contains functions binded from the Assimp C++ API.
"""


from ._assimp import lib, ffi


def assimp_import_from_bytes(bytes_in, optimize_graph, optimize_meshes):
    """
    @fixme doc
    """

    optimization_flags = 0
    if optimize_graph: 
        optimization_flags |= lib.OPTIMIZATION_FLAG_GRAPH
    if optimize_meshes: 
        optimization_flags |= lib.OPTIMIZATION_FLAG_MESHES

    scene = lib.assimp_import_from_bytes(
        bytes_in,
        len(bytes_in),
        optimization_flags
        )

    if scene.assimp_scene == ffi.NULL:
        raise ValueError("Invalid model: Assimp was not able to import the model")  # noqa

    return scene


def assimp_export_to_bytes(scene, output_format):
    """
    @fixme doc
    """

    if output_format not in ("glb", "gltf"):
        raise ValueError("Invalid output format: should be glb or gltf but is %s" % output_format)  # noqa

    output_format_dict = dict({
            "glb": lib.OUTPUT_FORMAT_GLB,
            "gltf": lib.OUTPUT_FORMAT_GLTF
        })

    bytes_out_p = ffi.new("char**")
    bytes_out_p_gc = ffi.gc(bytes_out_p, lib.assimp_free_bytes)

    length = lib.assimp_export_to_bytes(
        scene,
        output_format_dict[output_format],
        bytes_out_p
        )

    if length == 0:
        raise ValueError("Invalid model: Assimp was not able to export")

    bytes_out = ffi.cast("char*", bytes_out_p_gc[0])
    return ffi.unpack(bytes_out, length)
