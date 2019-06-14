#!python
# import a ESRI shape to vulcan objects
# input_shp: path to the shape file (the auxiliary files must also exist)
# object_layer: (optional) attribute that will be used as object layer
# object_name: (optional) attribute that will be used as object name
# object_group: (optional) attribute that will be used as object group
# output_dgd: path to a new or existing dgd where the data will be saved
# v1.0 05/2019 paulo.ernesto
'''
usage: $0 input_shp*shp layer:input_shp name:input_shp group:input_shp feature:input_shp output_dgd*dgd.isis
'''

'''
Copyright 2019 Vale

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

*** You can contribute to the main repository at: ***

https://github.com/pemn/vulcan_shape_export_import
---------------------------------

'''

import sys, os.path
import re

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui

def obj_import_shape(input_shp, object_layer, object_name, object_group, object_feature, output_dgd):
  import shapefile
  print("obj_import_shape")

  shapes = shapefile.Reader(input_shp)
  
  # fields = dict([(shapes.fields[i][0], i-1) for i in range(1, len(shapes.fields))])

  import vulcan

  dgd = None
  if os.path.exists(output_dgd):
    dgd = vulcan.dgd(output_dgd, 'w')
  else:
    dgd = vulcan.dgd(output_dgd, 'c')

  layer_name = object_layer
  layers = dict()
  for item in shapes.shapeRecords():
    point_type = int(not re.search('POINT', item.shape.shapeTypeName))

    coordinates = [tuple(_) + (0,0,point_type) for _ in item.shape.points]

    obj = vulcan.polyline(coordinates)

    # object without a valid layer name will have this default layer
    layer_name = '0'
    fields = item.record.as_dict()

    if object_layer in fields and fields[object_layer]:
      layer_name = str(fields[object_layer])
    elif object_layer:
      layer_name = object_layer

    if object_name in fields:
      obj.set_name(str(fields[object_name]))
    if object_group in fields:
      obj.set_group(str(fields[object_group]))
    if object_feature in fields:
      obj.set_group(str(fields[object_feature]))

    if layer_name not in layers:
      layers[layer_name] = vulcan.layer(layer_name)

    layers[layer_name].append(obj)

  for layer_obj in layers.values():
    dgd.save_layer(layer_obj)

main = obj_import_shape

if __name__=="__main__":
  usage_gui(__doc__)
