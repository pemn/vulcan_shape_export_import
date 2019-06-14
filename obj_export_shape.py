#!python
# export vulcan objects to a ESRI shape
# input_dgd: path to a new or existing dgd where the data will be saved
# input_layers: layer(s) containg the objects to be exported
# output_shp: path to the shape file (the auxiliary files must also exist)
# v1.0 05/2019 paulo.ernesto
'''
usage: $0 input_dgd*dgd.isis input_layers#layer:input_dgd output_shp*shp
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

# import modules from a pyz (zip) file with same name as scripts
sys.path.append(os.path.splitext(sys.argv[0])[0] + '.pyz')

from _gui import usage_gui

def obj_export_shape(input_dgd, input_layers, output_shp):
  print("obj_export_shape")
  import shapefile
  import vulcan

  shpw = shapefile.Writer(os.path.splitext(output_shp)[0])
  shpw.field('layer', 'C')
  shpw.field('name', 'C')
  shpw.field('group', 'C')
  shpw.field('feature', 'C')
  shpw.field('description', 'C')
  shpw.field('colour', 'N')

  dgd = vulcan.dgd(input_dgd, 'w')
  for layer_name in input_layers.split(';'):
    if not dgd.is_layer(layer_name):
      continue

    layer = dgd.get_layer(layer_name)
    for obj in layer:
      print(layer_name, obj.get_name())
      # if obj.num_points() == 1:
      #   p = obj.get_point(0)
      #   shpw.pointz(p.get_x(), p.get_y(), p.get_z())
      #   # shpw.null()
      # elif obj.num_points() == 2:
      #   # shpw.linez([])
      #   shpw.null()
      shpw.polyz([obj.coordinates])
      shpw.record(layer_name, obj.get_name(), obj.get_group(), obj.get_feature(), obj.get_description(), obj.get_colour())
  
  shpw.close()

main = obj_export_shape

if __name__=="__main__":
  usage_gui(__doc__)
