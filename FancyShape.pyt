import arcpy
import utilities
import conversion
import near

#
# Features in future versions:
# Near, Erase
#


class Toolbox(object):
    def __init__(self):
        self.label = "FancyShape"
        self.alias = "fancyshape"

        # List of tool classes associated with this toolbox
        self.tools = [Polygon2Line, Line2Polygon, Feature2Point, NewLayerVersion, Point2GPX, Near]


class Polygon2Line(object):
    def __init__(self):
        self.label = "Polygon to Line"
        self.description = "Converts a polygon feature class into a polyline feature class."
        self.canRunInBackground = False
        self.category = 'Data Management Tools\\Features'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_features = arcpy.Parameter(
            displayName='Output Features',
            name='out_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Output'
        )
        parameters = [in_features, out_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        conversion.polygon_2_line(in_features, out_features)


class Line2Polygon(object):
    def __init__(self):
        self.label = "Line to Polygon"
        self.description = "Converts a polyline feature class into a polygon feature class."
        self.canRunInBackground = False
        self.category = 'Data Management Tools\\Features'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_features = arcpy.Parameter(
            displayName='Output Features',
            name='out_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Output'
        )
        parameters = [in_features, out_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        conversion.line_2_polygon(in_features, out_features)


class Feature2Point(object):
    def __init__(self):
        self.label = "Feature to Point"
        self.description = "Converts any feature class into a point feature class."
        self.canRunInBackground = False
        self.category = 'Data Management Tools\\Features'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_features = arcpy.Parameter(
            displayName='Output Features',
            name='out_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Output'
        )
        parameters = [in_features, out_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        conversion.feature_2_point(in_features, out_features)


class NewLayerVersion(object):
    def __init__(self):
        self.label = "Create New Layer Version"
        self.description = "Creates a dated new version of the input layers."
        self.canRunInBackground = False
        self.category = 'Utilities'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input',
            multiValue=True
        )
        parameters = [in_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        utilities.create_layer_version(in_features)


class Point2GPX(object):
    def __init__(self):
        self.label = "Point to GPX"
        self.description = "Converts point feature class to GPX file."
        self.canRunInBackground = False
        self.category = 'Conversion Tools'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_file = arcpy.Parameter(
            displayName='Output GPX file',
            name='out_file',
            datatype='DEFile',
            parameterType='Required',
            direction='Output'
        )
        name_tag = arcpy.Parameter(
            displayName='Name tag',
            name='name_tag',
            datatype='GPString',
            parameterType='Required',
            direction='Output'

        )
        parameters = [in_features, out_file, name_tag]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_file = parameters[1].valueAsText
        name_tag = parameters[2].valueAsText

        utilities.project_better(in_features, 'in_memory\\features_proj', arcpy.SpatialReference(4326))
        with open(out_file, 'w+') as output:
            cur = arcpy.da.SearchCursor('in_memory\\features_proj', ['SHAPE@XY', name_tag])
            output.writelines("""<?xml version=\"1.0\" ?>
<gpx creator=\"Fancyshape\" version=\"1.1\">""")
            for row in cur:
                output.writelines("""  <wpt lat=\"{1}\" lon=\"{0}\">
    <ele>0</ele>
    <time> </time>
    <name>{2}</name>
    <desc> </desc>
  </wpt>""".format(row[0][0], row[0][1], row[1]))

            output.writelines("</gpx>")


class Near(object):
    def __init__(self):
        self.label = "Near"
        self.description = "Calculates distance between the input features and the " \
                           "closest feature in another layer or feature class."
        self.canRunInBackground = False
        self.category = 'Analysis Toolbox\\Proximity'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        near_features = arcpy.Parameter(
            displayName='Near Features',
            name='near_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        parameters = [in_features, near_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        near.near_tool(in_features, out_features)
