# Wavefront OBJ cleaner for Tabletop Simulator

This program performs some file-size optimizations on OBJ files exported from Blender for import into Tabletop Simulator (TTS) as a custom model. Additionally it works around a normal-parsing bug in TTS's OBJ parser.

### Optimizations

Each are optional:

- Drop superfluous leading/trailing zeros in coords
- Round coords to reduce digits
- Deduplicate elements (e.g. multiple `vt` entries with identical coords)
- Strip comments and elements ignored by TTS (e.g. materials)

### Workaround for TTS bug

Split normals are where a vertex shared by multiple faces has a different normal per face. Blender and other modeling tools use split normals to achieve hard-shaded edges without separating faces topologically (duplicating vertices/edges). The Wavefront OBJ format supports split normals by allowing each face to specify a unique normal (and UV for seams) for its vertices while allowing faces to share the vertex elements. Blender's OBJ export feature takes advantage of this support.

In contrast, game engines typically internally require each vertex to have a single normal and UV. Thus OBJ parsers for such engines duplicate vertices/edges in memory at hard-shaded edges and UV seams, so each vertex copy can have a single normal and UV. TTS uses the Unity game engine, and Unity Editor's OBJ viewer correctly performs this duplication. But TTS supports runtime import of OBJ files using different code, likely not provided by Unity.

Unfortunately TTS's OBJ importer has a bug in its vertex-duplication logic. It only correctly duplicates a vertex when the faces using it assign different UVs (e.g. a UV seam). It fails to duplicate a vertex when the faces using it only assign different normals but the same UV. Note that in that case it doesn't average the different normals for such a vertex, but completely discards all but the first normal. As a result, all faces using that vertex use the normal from just one face, and edges that are correctly hard-shaded in Blender and Unity Editor appear in TTS to be smoothed but in a distorted way: one face may appear flat while its neighbor appears curved. The effect is dependent on the order in which the faces are listed in the OBJ, not to be confused by the winding order in which vertices are listed for a particular face.

For reference, here is another runtime OBJ importer for Unity that correctly duplicates vertices when either the normals or UVs differ among the faces using it:
https://forum.unity.com/threads/free-runtime-obj-loader.365884/

To work around this bug in TTS's importer, obj_cleaner optionally pre-duplicates vertices (after any de-duplication performed by the optimization options) only where TTS would fail to do so, namely where the UVs match but the normals don't.

Note that in many cases, in Blender, one can instead use the deprecated Edge Split modifier or the Mesh Split tool to duplicate the vertices before OBJ export. However, that approach has a number of drawbacks, such as discarding custom normals for any split edges, choosing to split edges based on face-angle instead of whether the normals actually differ, and modifying topology (except when the modifier is left staged). Blender expects OBJ importers to follow at least the basic OBJ spec and duplicate vertices if needed by a renderer, so its split tools are designed for other use cases.

Thus obj_cleaner is a cleaner and more-targeted workaround for just the TTS OBJ import bug.
