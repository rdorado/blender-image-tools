import inspect
import bpy
import blf
import bpy_types
import sys
import os
import cycles
import mathutils

'''
allowed = {
   bpy.types.BlendData: ['actions', 'armatures', 'bl_rna', 'brushes', 'cameras', 'collections', 'curves', 'fonts', 'grease_pencils',
          'hair_curves', 'images', 'is_dity', 'is_saved', 'lattices', 'libraries', 'lightprobes', 'lights',
          'linestyles', 'masks', 'materials', 'meshes', 'metaballs', 'movieclips', 'node_groups', 'objects',
          'paint_curves', 'palettes', 'particles', 'paintclouds', 'rna_type', 'scenes', 'screens', 'shape_keys',
          'sounds', 'speakers', 'texts', 'textures', 'workspaces', 'worlds'], 
   bpy_types.Context: ['active_action', 'active_annotation_layer', 'active_bone', 'active_editable_fcurve',
          'active_gpencil_frame', 'active_gpencil_layer', 'active_nla_strip', 'active_nla_track', 'active_object', 'active_operator',
          'active_pose_bone', 'active_sequence_strip', 'annotation_data', 'annotation_data_owner', 'area', 'asset_file_handle',
          'asset_library_ref', 'bl_rna', 'blend_data', 'collection', 'copy', 'edit_object', 'editable_bones', 'editable_fcurves',
          'editable_gpencil_layers', 'editable_gpencil_strokes', 'editable_objects', 'engine', 'evaluated_depsgraph_get',
          'gizmo_group', 'gpencil_data', 'gpencil_data_owner', 'image_paint_object', 'layer_collection', 'mode', 'object',
          'objects_in_mode', 'objects_in_mode_unique_data', 'particle_edit_object', 'path_resolve', 'pose_object', 'preferences',
          'region', 'region_data', 'rna_type', 'scene', 'screen', 'sculpt_object', 'selectable_objects', 'selected_bones',
          'selected_editable_actions', 'selected_editable_bones', 'selected_editable_fcurves', 'selected_editable_keyframes',
          'selected_editable_objects', 'selected_editable_sequences', 'selected_movieclip_tracks', 'selected_nla_strips',
          'selected_objects', 'selected_pose_bones', 'selected_pose_bones_from_active_object', 'selected_sequences',
          'selected_visible_actions', 'selected_visible_fcurves', 'sequences', 'space_data', 'temp_override', 'tool_settings',
          'ui_list', 'vertex_paint_object', 'view_layer', 'visible_bones', 'visible_fcurves', 'visible_gpencil_layers',
          'visible_objects', 'visible_pose_bones', 'weight_paint_object', 'window', 'window_manager', 'workspace']}
'''

'''
   bpy_types.Context: [],
   bpy.types.BlendData: ['description', 'functions', 'identifier', 'name', 'name_property',
          'nested', 'properties', 'property_tags', 'translation_context'],
   bpy.types.Struct: ['description', 'functions', 'identifier', 'name', 'name_property', 'nested', 'properties',
          'property_tags', 'translation_context'],
   bpy.types.StringProperty: [ 'default', 'description', 'icon', 'identifier', 'is_animatable', 'is_argument_optional',
          'is_enum_flag', 'is_hidden', 'is_library_editable', 'is_never_none', 'is_output', 'is_overridable',
          'is_path_output', 'is_readonly', 'is_registered', 'is_registered_optional', 'is_required', 'is_runtime',
          'is_skip_save', 'length_max', 'name', 'srna', 'subtype', 'tags', 'translation_context', 'type', 'unit']
 '''

allowed = {
   bpy.types.Area:['height', 'regions', 'show_menus', 'spaces', 'type', 'ui_type',
          'width', 'x', 'y'],
   bpy.types.BlendData: ['actions', 'armatures', 'brushes', 'cameras', 'collections', 'curves', 'fonts', 'grease_pencils',
          'hair_curves', 'images', 'is_dity', 'is_saved', 'lattices', 'libraries', 'lightprobes', 'lights',
          'linestyles', 'masks', 'materials', 'meshes', 'metaballs', 'movieclips', 'node_groups', 'objects',
          'paint_curves', 'palettes', 'particles', 'paintclouds', 'scenes', 'screens', 'shape_keys',
          'sounds', 'speakers', 'texts', 'textures', 'workspaces', 'worlds'],
   bpy.types.BoolProperty: ['array_dimensions', 'array_length', 'default', 'default_array', 'description', 'icon', 'identifier',
          'is_animatable', 'is_argument_optional', 'is_array', 'is_enum_flag', 'is_hidden', 'is_library_editable',
          'is_never_none', 'is_output', 'is_overridable', 'is_path_output', 'is_readonly', 'is_registered', 'is_registered_optional',
          'is_required', 'is_runtime', 'is_skip_save', 'name', 'srna', 'subtype', 'tags', 'translation_context', 'type', 'unit'],
   bpy.types.Camera: ['angle', 'angle_x', 'angle_y', 'animation_data', 'asset_data',
          'background_images', 'clip_end', 'clip_start', 'cycles', 'display_size', 'dof',
          'is_embedded_data', 'is_evaluated', 'is_library_indirect', 'is_missing',
          'is_runtime_data', 'lens', 'lens_unit', 'library', 'library_weak_reference',
          'name', 'name_full', 'ortho_scale', 'override_library', 'passepartout_alpha', 'preview',
          'sensor_fit', 'sensor_height', 'sensor_width', 'shift_x', 'shift_y', 'show_background_images',
          'show_composition_center', 'show_composition_center_diagonal', 'show_composition_golden',
          'show_composition_golden_tria_a', 'show_composition_golden_tria_b', 'show_composition_harmony_tri_a',
          'show_composition_harmony_tri_b', 'show_composition_thirds', 'show_limits', 'show_mist', 'show_name',
          'show_passepartout', 'show_safe_areas', 'show_safe_center', 'show_sensor', 'stereo', 'tag', 'type',
          'use_extra_user', 'use_fake_user', 'users'],
   bpy.types.CameraDOFSettings: ['aperture_blades', 'aperture_fstop', 'aperture_ratio', 'aperture_rotation',
          'focus_distance', 'focus_object', 'focus_subtarget', 'use_dof'],
   bpy.types.CameraStereoData: ['convergence_distance', 'convergence_mode', 'interocular_distance', 'pivot',
          'pole_merge_angle_from', 'pole_merge_angle_to', 'rna_type', 'use_pole_merge', 'use_spherical_stereo'],
   bpy.types.CollectionProperty: ['description', 'fixed_type', 'icon', 'identifier', 'is_animatable', 'is_argument_optional',
          'is_enum_flag', 'is_hidden', 'is_library_editable', 'is_never_none', 'is_output', 'is_overridable', 'is_path_output',
          'is_readonly', 'is_registered', 'is_registered_optional', 'is_required', 'is_runtime', 'is_skip_save', 'name',
          'srna', 'subtype', 'tags', 'translation_context', 'type', 'unit'],
   bpy.types.CollisionSettings: ['absorption', 'cloth_friction', 'damping', 'damping_factor', 'damping_random',
          'friction_factor', 'friction_random', 'permeability', 'stickiness', 'thickness_inner',
          'thickness_outer', 'use', 'use_culling', 'use_normal', 'use_particle_kill'],
   bpy.types.EnumProperty: [
          #'default',
          'default_flag', 'description', 
          #'enum_items', 'enum_items_static', 'enum_items_static_ui',
          'icon',
          'identifier', 'is_animatable', 'is_argument_optional', 'is_enum_flag', 'is_hidden', 'is_library_editable', 'is_never_none',
          'is_output', 'is_overridable', 'is_path_output', 'is_readonly', 'is_registered', 'is_registered_optional', 'is_required',
          'is_runtime', 'is_skip_save', 'name', 'srna', 'subtype', 'tags', 'translation_context', 'type', 'unit'],
   bpy.types.EnumPropertyItem: [ 'description', 'functions', 'identifier', 'name', 'name_property', 'nested', 'properties', 'property_tags', 'translation_context'],
   bpy.types.FieldSettings: ['apply_to_location', 'apply_to_rotation', 'distance_max', 'distance_min', 
          'falloff_power', 'falloff_type', 'flow', 'guide_clump_amount', 'guide_clump_shape', 'guide_free',
          'guide_kink_amplitude', 'guide_kink_axis', 'guide_kink_frequency', 'guide_kink_shape', 'guide_kink_type',
          'guide_minimum', 'harmonic_damping', 'inflow', 'linear_drag', 'noise', 'quadratic_drag', 'radial_falloff',
          'radial_max', 'radial_min', 'rest_length', 'seed', 'shape', 'size', 'source_object', 'strength',
          'texture', 'texture_mode', 'texture_nabla', 'type', 'use_2d_force', 'use_absorption', 'use_global_coords',
          'use_gravity_falloff', 'use_guide_path_add', 'use_guide_path_weight', 'use_max_distance', 'use_min_distance',
          'use_multiple_springs', 'use_object_coords', 'use_radial_max', 'use_radial_min', 'use_root_coords',
          'use_smoke_density', 'wind_factor', 'z_direction'],
   bpy.types.Function: ['description', 'functions', 'identifier', 'name', 'name_property', 'nested', 'properties', 'property_tags', 'translation_context'],
   bpy.types.ImagePreview: ['icon_id', 'icon_pixels', 'icon_pixels_float', 'icon_size', 'image_pixels',
          'image_pixels_float', 'image_size', 'is_icon_custom', 'is_image_custom'],
   bpy.types.Material: ['alpha_threshold', 'animation_data',
          'asset_data', 'blend_method', 'cycles', 'diffuse_color', 'grease_pencil',
          'is_embedded_data', 'is_evaluated', 'is_grease_pencil', 'is_library_indirect', 'is_missing',
          'is_runtime_data', 'library', 'library_weak_reference', 'line_color', 'line_priority',
          'lineart', 'metallic', 'name', 'name_full', 'node_tree',
          'override_library', 'paint_active_slot', 'paint_clone_slot', 'pass_index', 'preview',
          'preview_render_type', 'refraction_depth', 'roughness', 'shadow_method', 'show_transparent_back',
          'specular_color', 'specular_intensity', 'tag', 'texture_paint_images', 'texture_paint_slots',
          'use_backface_culling', 'use_extra_user', 'use_fake_user', 'use_nodes',
          'use_preview_world', 'use_screen_refraction', 'use_sss_translucency', 'users'],
   bpy.types.MaterialGPencilStyle: ['alignment_mode', 'alignment_rotation', 'color', 'fill_color',
          'fill_image', 'fill_style', 'flip', 'ghost', 'gradient_type', 'hide', 'is_fill_visible',
          'is_stroke_visible', 'lock', 'mix_color', 'mix_factor', 'mix_stroke_factor', 'mode',
          'pass_index', 'pixel_size', 'rna_type', 'show_fill', 'show_stroke', 'stroke_image',
          'stroke_style', 'texture_angle', 'texture_clamp', 'texture_offset', 'texture_scale',
          'use_fill_holdout', 'use_overlap_strokes', 'use_stroke_holdout'],
   bpy.types.MaterialLineArt: ['intersection_priority', 'mat_occlusion', 'use_intersection_priority_override', 'use_material_mask', 'use_material_mask_bits'],
   bpy.types.MeshUVLoopLayer: ['active', 'active_clone', 'active_render', 'data', 'edge_selection', 'name', 'pin', 'uv', 'vertex_selection'],
   bpy.types.NodeLink: ['from_node', 'from_socket', 'is_hidden', 'is_muted', 'is_valid', 'to_node', 'to_socket'],
   bpy.types.NodeSocketColor: ['bl_idname', 'bl_label', 'bl_subtype_label', 'default_value', 'description', 'display_shape', 
          'enabled', 'hide', 'hide_value', 'identifier', 'is_linked', 'is_multi_input', 'is_output', 'is_unavailable',
          'label', 'link_limit', 'name', 'show_expanded', 'type'],
   bpy.types.NodeSocketFloat: ['bl_idname', 'bl_label', 'bl_subtype_label', 'default_value', 'description', 'display_shape',
          'enabled', 'hide', 'hide_value', 'identifier', 'is_linked', 'is_multi_input', 'is_output', 'is_unavailable',
          'label', 'link_limit', 'name', 'show_expanded', 'type'],
   bpy.types.NodeSocketShader: ['bl_idname', 'bl_label', 'bl_subtype_label', 'description', 'display_shape',
          'enabled', 'hide', 'hide_value', 'identifier', 'is_linked', 'is_multi_input', 'is_output',
          'is_unavailable', 'label', 'link_limit', 
          'name', 'show_expanded', 'type'
          ],
   bpy.types.PointerProperty: ['description', 'fixed_type', 'icon', 'identifier', 'is_animatable', 'is_argument_optional',
          'is_enum_flag', 'is_hidden', 'is_library_editable', 'is_never_none', 'is_output', 'is_overridable', 'is_path_output',
          'is_readonly', 'is_registered', 'is_registered_optional', 'is_required', 'is_runtime', 'is_skip_save', 'name', 'srna',
          'subtype', 'tags', 'translation_context', 'type', 'unit'],
   bpy.types.Property: ['description', 'functions', 'identifier', 'name', 'name_property', 'nested', 'properties', 'property_tags', 'translation_context'],
   bpy.types.Screen: ['areas', 'asset_data',
          'is_animation_playing',
          'is_embedded_data', 'is_evaluated', 'is_library_indirect', 'is_missing', 'is_runtime_data',
          'is_scrubbing', 'is_temporary', 'library', 'library_weak_reference', 'name',
          'name_full', 'override_library',
          'preview', 'show_fullscreen', 'show_statusbar',
          'tag', 'use_extra_user', 'use_fake_user', 'use_follow',
          'use_play_3d_editors', 'use_play_animation_editors', 'use_play_clip_editors', 'use_play_image_editors',
          'use_play_node_editors', 'use_play_properties_editors', 'use_play_sequence_editors',
          'use_play_spreadsheet_editors', 'use_play_top_left_3d_editor', 
          'users'],
   bpy.types.ShaderNodeBackground: ['bl_description', 'bl_height_default', 'bl_height_max', 'bl_height_min', 'bl_icon',
          'bl_idname', 'bl_label', 'bl_static_type', 'bl_width_default', 'bl_width_max', 'bl_width_min', 'color',
          'dimensions', 'height', 'hide', 'inputs', 'internal_links',
          'label', 'location', 'mute', 'name', 'outputs', 'parent',
          'select', 'show_options', 'show_preview', 'show_texture',
          'type', 'use_custom_color', 'width', 'width_hidden'],
   bpy.types.ShaderNodeOutputMaterial: ['bl_description', 'bl_height_default', 'bl_height_max',
          'bl_height_min', 'bl_icon', 'bl_idname', 'bl_label', 'bl_static_type', 'bl_width_default',
          'bl_width_max', 'bl_width_min', 'color', 'dimensions', 'height', 'hide',
          'inputs', 'internal_links', 'is_active_output', 'label',
          'location', 'mute', 'name', 'outputs',
          'select', 'show_options', 'show_preview', 'show_texture', 'target',
          'type', 'use_custom_color', 'width', 'width_hidden'],
   bpy.types.ShaderNodeOutputWorld: ['bl_description', 'bl_height_default', 'bl_height_max', 'bl_height_min',
          'bl_icon', 'bl_idname', 'bl_label', 'bl_static_type', 'bl_width_default', 'bl_width_max',
          'bl_width_min', 'color', 'dimensions', 'height',
          'hide', 'inputs', 'internal_links', 'is_active_output',
          'label', 'location', 'mute', 'name', 'outputs', 'parent',
          'select', 'show_options', 'show_preview', 'show_texture', 'target', 'type',
          'use_custom_color', 'width', 'width_hidden'],
   bpy.types.ShaderNodeBsdfPrincipled: ['bl_description', 'bl_height_default', 'bl_height_max',
          'bl_height_min', 'bl_icon', 'bl_idname', 'bl_label', 'bl_static_type',
          'bl_width_default', 'bl_width_max', 'bl_width_min', 'color', 'dimensions',
          'distribution', 'height', 'hide',
          'inputs', 'internal_links', 'label', 'location', 'mute',
          'name', 'outputs', 'parent',
          'select', 'show_options', 'show_preview', 'show_texture',
          'subsurface_method', 'type', 'use_custom_color', 'width', 'width_hidden'],
   bpy.types.ShaderNodeTree: ['active_input', 'active_output', 'animation_data',
          'asset_data', 'bl_description', 'bl_icon', 'bl_idname',
          'bl_label', 'grease_pencil',
          'inputs', 'is_embedded_data', 'is_evaluated', 'is_library_indirect', 'is_missing',
          'is_runtime_data', 'library', 'library_weak_reference', 'links', 'name', 'name_full', 'nodes',
          'outputs', 'override_library', 
          'preview', 'tag', 'type', 'use_extra_user', 'use_fake_user',
          'users', 'view_center'
          ],
   bpy.types.SpaceView3D: ['camera', 'clip_end', 'clip_start', 'icon_from_show_object_viewport', 'lens',
          'local_view', 'lock_bone', 'lock_camera', 'lock_cursor', 'lock_object', 'mirror_xr_session',
          'overlay', 'region_3d', 'region_quadviews', 'render_border_max_x', 'render_border_max_y',
          'render_border_min_x', 'render_border_min_y', 'rna_type', 'shading', 'show_bundle_names',
          'show_camera_path', 'show_gizmo', 'show_gizmo_camera_dof_distance', 'show_gizmo_camera_lens',
          'show_gizmo_context', 'show_gizmo_empty_force_field', 'show_gizmo_empty_image',
          'show_gizmo_light_look_at', 'show_gizmo_light_size', 'show_gizmo_navigate',
          'show_gizmo_object_rotate', 'show_gizmo_object_scale', 'show_gizmo_object_translate',
          'show_gizmo_tool', 'show_locked_time', 'show_object_select_armature', 'show_object_select_camera',
          'show_object_select_curve', 'show_object_select_curves', 'show_object_select_empty',
          'show_object_select_font', 'show_object_select_grease_pencil', 'show_object_select_lattice',
          'show_object_select_light', 'show_object_select_light_probe', 'show_object_select_mesh',
          'show_object_select_meta', 'show_object_select_pointcloud', 'show_object_select_speaker',
          'show_object_select_surf', 'show_object_select_volume', 'show_object_viewport_armature',
          'show_object_viewport_camera', 'show_object_viewport_curve', 'show_object_viewport_curves',
          'show_object_viewport_empty', 'show_object_viewport_font', 'show_object_viewport_grease_pencil',
          'show_object_viewport_lattice', 'show_object_viewport_light', 'show_object_viewport_light_probe',
          'show_object_viewport_mesh', 'show_object_viewport_meta', 'show_object_viewport_pointcloud',
          'show_object_viewport_speaker', 'show_object_viewport_surf', 'show_object_viewport_volume',
          'show_reconstruction', 'show_region_header', 'show_region_hud', 'show_region_tool_header',
          'show_region_toolbar', 'show_region_ui', 'show_stereo_3d_cameras', 'show_stereo_3d_convergence_plane',
          'show_stereo_3d_volume', 'show_viewer', 'stereo_3d_camera', 'stereo_3d_convergence_plane_alpha',
          'stereo_3d_eye', 'stereo_3d_volume_alpha', 'tracks_display_size', 'tracks_display_type', 'type',
          'use_local_camera', 'use_local_collections', 'use_render_border'],
   bpy.types.StringProperty: ['default', 'description', 'icon', 'identifier', 'is_animatable',
          'is_argument_optional', 'is_enum_flag', 'is_hidden', 'is_library_editable', 'is_never_none',
          'is_output', 'is_overridable', 'is_path_output', 'is_readonly', 'is_registered',
          'is_registered_optional', 'is_required', 'is_runtime', 'is_skip_save', 'length_max',
          'name', 'srna', 'subtype', 'tags', 'translation_context', 'type', 'unit'],
   bpy.types.Struct: ['description', 'functions', 'identifier', 'name', 'name_property', 'nested', 'properties',
          'property_tags', 'translation_context'],
   bpy.types.World: ['animation_data', 'asset_data', 'color', 'cycles', 'cycles_visibility', 
          'is_embedded_data', 'is_evaluated', 'is_library_indirect', 'is_missing', 'is_runtime_data', 'library',
          'library_weak_reference', 'light_settings', 'lightgroup', 'mist_settings', 'name', 'name_full',
          'node_tree',
          'override_library',
          'preview', 'tag', 'use_extra_user', 'use_fake_user', 'use_nodes',
          'users'],
   bpy.types.WorldLighting: ['ao_factor', 'distance', 'use_ambient_occlusion'],
   bpy.types.WorldMistSettings: ['depth', 'falloff', 'height', 'intensity', 'start', 'use_mist'],
   bpy_types.Mesh: ['animation_data',
          'asset_data', 'attributes', 'auto_smooth_angle',
          'auto_texspace',
          'color_attributes', 'corner_normals',
          #'cycles',
          'edge_creases', 'edge_keys', 'edges',
          'face_maps',
          'has_bevel_weight_edge', 'has_bevel_weight_vertex', 'has_crease_edge', 'has_crease_vertex',
          'has_custom_normals', 'is_editmode', 'is_embedded_data', 'is_evaluated', 'is_library_indirect',
          'is_missing', 'is_runtime_data', 'library', 'library_weak_reference', 'loop_triangle_polygons',
          'loop_triangles', 'loops', 'materials', 'name', 'name_full',
          'override_library', 'polygon_layers_float', 'polygon_layers_int',
          'polygon_layers_string', 'polygon_normals', 'polygons', 'preview', 'remesh_mode',
          'remesh_voxel_adaptivity', 'remesh_voxel_size', 'rna_type', 'sculpt_vertex_colors',
          'shape_keys', 'skin_vertices', 'tag', 'texco_mesh', 'texspace_location',
          'texspace_size', 'texture_mesh', 'total_edge_sel', 'total_face_sel', 'total_vert_sel',
          'use_auto_smooth', 'use_auto_texspace',
          'use_extra_user', 'use_fake_user', 'use_mirror_topology', 'use_mirror_vertex_groups', 'use_mirror_x',
          'use_mirror_y', 'use_mirror_z', 'use_paint_mask', 'use_paint_mask_vertex', 'use_remesh_fix_poles',
          'use_remesh_preserve_paint_mask', 'use_remesh_preserve_sculpt_face_sets',
          'use_remesh_preserve_vertex_colors', 'use_remesh_preserve_volume',
          'users', 'uv_layer_clone', 'uv_layer_clone_index', 'uv_layer_stencil', 'uv_layer_stencil_index',
          'uv_layers', 'vertex_colors', 'vertex_creases',
          'vertex_layers_float', 'vertex_layers_int', 'vertex_layers_string', 'vertex_normals',
          'vertex_paint_masks', 'vertices'],
   bpy_types.Object: ['active_material', 'active_material_index', 'active_shape_key', 'active_shape_key_index',
          'add_rest_position_attribute', 'animation_data',
          'asset_data', 'bound_box', 'children',
          'children_recursive', 'collision', 'color', 'constraints',
          'cycles', 'data', 'delta_location',
          'delta_rotation_euler', 'delta_rotation_quaternion', 'delta_scale', 'dimensions', 'display',
          'display_bounds_type', 'display_type', 'empty_display_size', 'empty_display_type',
          'empty_image_depth', 'empty_image_offset', 'empty_image_side', 'face_maps',
          'field', 'grease_pencil_modifiers',
          'hide_render', 'hide_select', 'hide_viewport', 'image_user',
          'instance_collection', 'instance_faces_scale', 'instance_type',
          'is_embedded_data', 'is_evaluated', 'is_from_instancer', 'is_from_set',
          'is_holdout', 'is_instancer', 'is_library_indirect', 'is_missing', 'is_runtime_data',
          'is_shadow_catcher', 'library', 'library_weak_reference', 'lightgroup', 'lineart',
          'location', 'lock_location', 'lock_rotation', 'lock_rotation_w', 'lock_rotations_4d',
          'lock_scale', 'material_slots', 'matrix_basis', 'matrix_local', 'matrix_parent_inverse',
          'matrix_world', 'mode', 'modifiers', 'motion_path', 'name', 'name_full',
          'override_library', 'parent', 'parent_bone',
          'parent_type', 'parent_vertices', 'particle_systems', 'pass_index', 'pose', 'preview',
          'rigid_body', 'rigid_body_constraint', 'rotation_axis_angle', 'rotation_euler',
          'rotation_mode', 'rotation_quaternion', 'scale', 'shader_effects',
          'show_all_edges', 'show_axis', 'show_bounds',
          'show_empty_image_only_axis_aligned', 'show_empty_image_orthographic', 'show_empty_image_perspective',
          'show_in_front', 'show_instancer_for_render', 'show_instancer_for_viewport', 'show_name',
          'show_only_shape_key', 'show_texture_space', 'show_transparent', 'show_wire', 'soft_body', 'tag',
          'track_axis', 'type', 'up_axis',
          'use_camera_lock_parent', 'use_dynamic_topology_sculpting',
          'use_empty_image_alpha', 'use_extra_user', 'use_fake_user', 'use_grease_pencil_lights',
          'use_instance_faces_scale', 'use_instance_vertices_rotation', 'use_mesh_mirror_x',
          'use_mesh_mirror_y', 'use_mesh_mirror_z', 'use_shape_key_edit_mode', 'use_simulation_cache',
          'users', 'users_collection', 'users_scene', 'vertex_groups',
          'visible_camera', 'visible_diffuse', 'visible_glossy',
          'visible_shadow', 'visible_transmission', 'visible_volume_scatter'],
   bpy.types.ObjectDisplay: ['show_shadows'],
   bpy.types.ObjectLineArt: ['crease_threshold', 'intersection_priority', 'usage', 'use_crease_override', 'use_intersection_priority_override'],
   bpy.types.PointLight: ['animation_data',
          'asset_data', 'color', 'constant_coefficient',
          'contact_shadow_bias', 'contact_shadow_distance', 'contact_shadow_thickness', 'cutoff_distance',
          'cycles',
          'diffuse_factor', 'distance', 'energy',
          'falloff_type', 'is_embedded_data', 'is_evaluated', 'is_library_indirect', 'is_missing',
          'is_runtime_data', 'library', 'library_weak_reference', 'linear_attenuation', 'linear_coefficient',
          'name', 'name_full', 'node_tree',
          'override_library', 'preview', 'quadratic_attenuation',
          'quadratic_coefficient', 'rna_type', 'shadow_buffer_bias', 'shadow_buffer_clip_start', 'shadow_buffer_samples',
          'shadow_buffer_size', 'shadow_color', 'shadow_soft_size', 'specular_factor', 'tag', 'type',
          'use_contact_shadow', 'use_custom_distance', 'use_extra_user', 'use_fake_user', 'use_nodes', 'use_shadow', 'users', 'volume_factor'],
   bpy.types.RegionView3D: [ 'clip_planes', 'is_orthographic_side_view', 'is_perspective', 'lock_rotation', 'perspective_matrix',
          'show_sync_view', 'use_box_clip', 'use_clip_planes', 'view_camera_offset', 'view_camera_zoom', 'view_distance',
          'view_location', 'view_matrix', 'view_perspective', 'view_rotation', 'window_matrix'],
   bpy.types.StudioLight: ['has_specular_highlight_pass', 'index', 'is_user_defined', 'light_ambient', 'name', 'path', 'path_irr_cache', 'path_sh_cache', 'solid_lights', 'spherical_harmonics_coefficients', 'type'],
   bpy.types.UserSolidLight: [ 'diffuse_color', 'direction', 'smooth', 'specular_color', 'use'],
   bpy.types.View3DOverlay: ['backwire_opacity', 'bone_wire_alpha', 'display_handle', 'fade_inactive_alpha', 'gpencil_fade_layer',
          'gpencil_fade_objects', 'gpencil_grid_opacity', 'gpencil_vertex_paint_opacity', 'grid_lines', 'grid_scale', 'grid_scale_unit',
          'grid_subdivisions', 'normals_constant_screen_size', 'normals_length', 'retopology_offset', 'rna_type',
          'sculpt_curves_cage_opacity', 'sculpt_mode_face_sets_opacity', 'sculpt_mode_mask_opacity', 'show_annotation', 'show_axis_x',
          'show_axis_y', 'show_axis_z', 'show_bones', 'show_cursor', 'show_curve_normals', 'show_edge_bevel_weight', 'show_edge_crease',
          'show_edge_seams', 'show_edge_sharp', 'show_edges', 'show_extra_edge_angle', 'show_extra_edge_length', 'show_extra_face_angle',
          'show_extra_face_area', 'show_extra_indices', 'show_extras', 'show_face_center', 'show_face_normals', 'show_face_orientation',
          'show_faces', 'show_fade_inactive', 'show_floor', 'show_freestyle_edge_marks', 'show_freestyle_face_marks', 'show_light_colors',
          'show_look_dev', 'show_motion_paths', 'show_object_origins', 'show_object_origins_all', 'show_onion_skins', 'show_ortho_grid',
          'show_outline_selected', 'show_overlays', 'show_paint_wire', 'show_relationship_lines', 'show_retopology',
          'show_sculpt_curves_cage', 'show_sculpt_face_sets', 'show_sculpt_mask', 'show_split_normals', 'show_stats', 'show_statvis',
          'show_text', 'show_vertex_normals', 'show_viewer_attribute', 'show_weight', 'show_wireframes', 'show_wpaint_contours',
          'show_xray_bone', 'texture_paint_mode_opacity', 'use_debug_freeze_view_culling', 'use_gpencil_canvas_xray',
          'use_gpencil_edit_lines', 'use_gpencil_fade_gp_objects', 'use_gpencil_fade_layers', 'use_gpencil_fade_objects',
          'use_gpencil_grid', 'use_gpencil_multiedit_line_only', 'use_gpencil_onion_skin', 'use_gpencil_show_directions',
          'use_gpencil_show_material_name', 'use_normals_constant_screen_size', 'vertex_opacity', 'vertex_paint_mode_opacity',
          'viewer_attribute_opacity', 'weight_paint_mode_opacity', 'wireframe_opacity', 'wireframe_threshold', 'xray_alpha_bone'],
   bpy.types.View3DShading: ['aov_name', 'background_color', 'background_type', 'cavity_ridge_factor', 'cavity_type',
          'cavity_valley_factor', 'color_type', 'curvature_ridge_factor', 'curvature_valley_factor', 
          #'cycles',
          'light', 'object_outline_color', 'render_pass', 'rna_type', 'selected_studio_light', 'shadow_intensity', 'show_backface_culling',
          'show_cavity', 'show_object_outline', 'show_shadows', 'show_specular_highlight', 'show_xray', 'show_xray_wireframe',
          'single_color', 'studio_light', 'studiolight_background_alpha', 'studiolight_background_blur', 'studiolight_intensity',
          'studiolight_rotate_z', 'type', 'use_compositor', 'use_dof', 'use_scene_lights', 'use_scene_lights_render',
          'use_scene_world', 'use_scene_world_render', 'use_studiolight_view_rotation', 'use_world_space_lighting',
          'wireframe_color_type', 'xray_alpha', 'xray_alpha_wireframe'],
   bpy_types.WorkSpace: ['active_pose_asset_index', 
          'asset_data', 'asset_library_ref',
          'is_embedded_data', 'is_evaluated', 'is_library_indirect',
          'is_missing', 'is_runtime_data', 'library', 'library_weak_reference', 'name',
          'name_full', 'object_mode',
          'override_library', 'owner_ids', 'preview',
          'screens', 'tag', 'tools',
          'use_extra_user', 'use_fake_user', 'use_filter_by_owner', 'use_pin_scene',
          'users'],
   mathutils.Color: ['b', 'g', 'h', 'hsv', 'is_frozen', 'is_valid', 'is_wrapped', 'r', 's', 'v'],
   mathutils.Euler: ['is_frozen', 'is_valid', 'is_wrapped', 'order', 'owner', 'x', 'y', 'z',],
   mathutils.Quaternion: ['angle', 'axis', 'is_frozen', 'is_valid', 'is_wrapped', 'magnitude',
          'owner', 'w', 'x', 'y', 'z'],
   mathutils.Matrix: ['is_frozen', 'is_identity', 'is_negative',
          'is_orthogonal', 'is_orthogonal_axis_vectors', 'is_valid', 'is_wrapped', 'median_scale',
          #'owner',
          'translation',],
   mathutils.Vector: ['is_frozen', 'is_valid', 'is_wrapped', 'length', 'length_squared', 'magnitude',
          #'owner', 
          'w', 'x', 'y', 'z',],
   cycles.properties.CyclesCameraSettings: ['fisheye_fov', 'fisheye_lens', 'fisheye_polynomial_k0',
          'fisheye_polynomial_k1', 'fisheye_polynomial_k2', 'fisheye_polynomial_k3', 'fisheye_polynomial_k4',
          'latitude_max', 'latitude_min', 'longitude_max', 'longitude_min', 'name', 'panorama_type'],
   cycles.properties.CyclesLightSettings: [ 'cast_shadow', 'is_caustics_light', 'is_portal', 'max_bounces', 'name', 'use_multiple_importance_sampling'],
   cycles.properties.CyclesMeshSettings: ['name'],
   cycles.properties.CyclesObjectSettings: ['ao_distance', 'dicing_rate', 'is_caustics_caster',
          'is_caustics_receiver', 'motion_steps', 'name',
          'shadow_terminator_geometry_offset', 'shadow_terminator_offset',
          'use_adaptive_subdivision', 'use_camera_cull', 'use_deform_motion', 'use_distance_cull',
          'use_motion_blur'],
   cycles.properties.CyclesMaterialSettings: ['displacement_method', 'emission_sampling',
          'homogeneous_volume', 'name', 'use_transparent_shadow', 'volume_interpolation',
          'volume_sampling', 'volume_step_rate'],
   cycles.properties.CyclesWorldSettings: ['camera', 'diffuse', 'glossy', 'name', 'scatter', 'shadow', 'transmission'],
   cycles.properties.CyclesView3DShadingSettings: [ 'name', 'render_pass', 'show_active_pixels'],
   cycles.properties.CyclesVisibilitySettings: [ 'camera', 'diffuse', 'glossy', 'name', 'scatter', 'shadow', 'transmission']
}


def instrospect(obj, elems_to_process, indent="  "):
    for (elem, elem_obj) in inspect.getmembers(obj):
        for elem_to_proc in elems_to_process:
            #print("-->", elems_to_process)
            if elem == elem_to_proc:
                if isinstance(elem_obj, bpy.types.bpy_prop_collection):
                    print(indent, elem, ": [", sep='')
                    for col_elem in elem_obj:
                        if type(col_elem) in allowed:
                            instrospect(col_elem, allowed[type(col_elem)], indent+"  ")
                        elif isinstance(col_elem, float) or isinstance(col_elem, int) or isinstance(col_elem, str) or isinstance(col_elem, bool) or col_elem == None:
                            print(indent+"  ", col_elem, sep='')
                        else:
                            print(dir(col_elem))
                            print(indent+"  ","  ", type(col_elem),col_elem)
                        #print(dir(col_elem))
                    print(indent, "],", sep='')
                elif  isinstance(elem_obj, bpy.types.bpy_prop_array) or isinstance(elem_obj, list):
                    t_arr = []
                    for obj in elem_obj:
                        if isinstance(obj, float) or isinstance(obj, int) or isinstance(obj, str) or isinstance(obj, bool) or obj == None:
                            t_arr.append(str(obj))
                        else:
                             print(dir(obj))
                             print(indent+"  ","  ", type(obj),obj)
                    print(indent+"  ",elem,": [",", ".join(t_arr) ,"]", sep='')
                elif type(elem_obj) in allowed:
                    print(indent, elem, ":", sep='')
                    #print(elem, type(elem_obj))
                    #print(dir(elem_obj))
                    instrospect(elem_obj, allowed[type(elem_obj)], indent+"  ")
                elif isinstance(elem_obj, float) or isinstance(elem_obj, int) or isinstance(elem_obj, str) or isinstance(elem_obj, bool) or elem_obj == None:
                    print(indent, "  ", elem, ": ", elem_obj, ",", sep='')
                elif isinstance(elem_obj, tuple) or isinstance(elem_obj, set):
                    print(indent, "  ", elem, ": ", elem_obj, ",", sep='')
                else:
                    print(dir(elem_obj))
                    raise Exception("Unknown type:", str(type(elem_obj)), "for property:", elem)
                    #    instrospect(col_elem)
                #print("\n", elem, "\n", type(elem_obj), "\n")
#        if elem2 in al_elems:
            #if isinstance(eltype2, bpy.types.bpy_prop_collection):
            #    for elem2_c in eltype2:
            #       print("\n\n",elem2_c,"\n",dir(elem2_c),"\n\n")
            #  else:
            #    print("\n\n",elem2,"\n",type(eltype2),"\n\n")

def print_usage():
    print("Usage: python '"+sys.argv[0]+"' <blender filename> <output filename>")
    print("Example: python "+sys.argv[0]+" cube.blend cube.dat")
    sys.exit(0)
    
def main():
    args = sys.argv[1:]
    if len(args) < 2: print_usage()

    # open blender file
    input_filename = args[0]
    bpy.ops.wm.open_mainfile(filepath=input_filename)

    #obj = bpy.context.active_object
    #for elem in ['app', 'context', 'data', 'msgbus', 'ops', 'path', 'props', 'types', 'utils']:
    
    for (elem, root_obj) in inspect.getmembers(bpy):
      
      for (root_atype, al_elems) in allowed.items():
        #print(type(root_obj))
        if isinstance(root_obj, root_atype):
          
          instrospect(root_obj, al_elems)
          #print("\n", elem, "\n", dir(root_obj), "\n")

'''
      #print("\n\n",elem,"\n",type(eltype),"\n\n")
      #getattr
    #


i = 0
for ob in bpy.data.objects:
    print("\n" + str(i) + ": " + str(ob.type))
    print(dir(ob.data))
    i=i+1
    if ob.type == 'MESH':
        print('MESH')
        #print(dir(ob.data.edges))
        print(' Vertices:')
        for v in ob.data.vertices:
            print(v.co)
        print(' Edges:')
        for e in ob.data.edges:
            #print(dir(e.vertices))
            print('  Edge:')            
            for v in e.vertices:
                print(v)
            #    #print(dir(v))
        #mesh_owners.setdefault(ob.data, []).append(ob)
'''

if __name__ == "__main__":
    sys.exit(main())