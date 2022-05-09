"""
Model exported as python.
Name : 06 Cc Network Metric
Group : Github
With QGIS : 31616
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
import processing


class CcNetworkMetric(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('Closeness', 'Closeness', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('CorrectedNetwork', 'Corrected Network', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Cc', 'Cc', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Meancc', 'meanCc', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centrecc', 'centreCc', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # Calculadora Cc
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Cc',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': 'case\r\n when \r\n \"closeness\" < mean( \"closeness\" ) - 2*stdev( \"closeness\" ) \r\n  then 2^1\r\n when \r\n \"closeness\" >= mean( \"closeness\" )- 2*stdev( \"closeness\" ) and \r\n \"closeness\" < mean( \"closeness\" ) - 1*stdev( \"closeness\" ) \r\n  then 2^2\r\n when \r\n \"closeness\" >= mean( \"closeness\" )- 1*stdev( \"closeness\" ) and \r\n \"closeness\" < mean( \"closeness\" ) + 0*stdev( \"closeness\" ) \r\n  then 2^3\r\n when \r\n \"closeness\" >= mean( \"closeness\" )+ 0*stdev( \"closeness\" ) and \r\n \"closeness\" < mean( \"closeness\" ) + 1*stdev( \"closeness\" ) \r\n  then 2^4\r\n when \r\n \"closeness\" >= mean( \"closeness\" ) + 1*stdev( \"closeness\" ) and \r\n \"closeness\" <  mean( \"closeness\" ) + 2*stdev( \"closeness\" ) \r\n  then 2^5\r\n when \r\n \"closeness\" >= mean( \"closeness\" ) + 2*stdev( \"closeness\" ) \r\n  then 2^6\r\n end',
            'INPUT': parameters['Closeness'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraCc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Rasterize Cc
        alg_params = {
            'BURN': 0,
            'DATA_TYPE': 5,
            'EXTENT': outputs['CalculadoraCc']['OUTPUT'],
            'EXTRA': '',
            'FIELD': 'Cc',
            'HEIGHT': 500,
            'INIT': None,
            'INPUT': outputs['CalculadoraCc']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 1,
            'WIDTH': 500,
            'OUTPUT': parameters['Cc']
        }
        outputs['RasterizeCc'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cc'] = outputs['RasterizeCc']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Raster Cc_centre
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '\"\'Rasterized\' from algorithm \'Rasterize Cc\'@1\" <= 4',
            'EXTENT': None,
            'LAYERS': outputs['RasterizeCc']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCc_centre'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Raster calc Cc_centre
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '(\"\'Output\' from algorithm \'Raster Cc_centre\'@1\"=0/\"\'Output\' from algorithm \'Raster Cc_centre\'@1\")+1',
            'EXTENT': None,
            'LAYERS': outputs['RasterCc_centre']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalcCc_centre'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RasterCalcCc_centre']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Raster Cc_mean
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '\"\'Rasterized\' from algorithm \'Rasterize Cc\'@1\" <= 8',
            'EXTENT': None,
            'LAYERS': outputs['RasterizeCc']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCc_mean'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': '$area = maximum($area)',
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Raster calc MeanCc
        alg_params = {
            'CELLSIZE': 0,
            'CRS': None,
            'EXPRESSION': '(\"\'Output\' from algorithm \'Raster Cc_mean\'@1\"=0/\"\'Output\' from algorithm \'Raster Cc_mean\'@1\")+1',
            'EXTENT': None,
            'LAYERS': outputs['RasterCc_mean']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalcMeancc'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Delete holes
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'MIN_AREA': 0,
            'OUTPUT': parameters['Centrecc']
        }
        outputs['DeleteHoles'] = processing.run('native:deleteholes', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centrecc'] = outputs['DeleteHoles']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RasterCalcMeancc']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': '$area = maximum($area)',
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Delete holes
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'MIN_AREA': 0,
            'OUTPUT': parameters['Meancc']
        }
        outputs['DeleteHoles'] = processing.run('native:deleteholes', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Meancc'] = outputs['DeleteHoles']['OUTPUT']
        return results

    def name(self):
        return '06 Cc Network Metric'

    def displayName(self):
        return '06 Cc Network Metric'

    def group(self):
        return 'Github'

    def groupId(self):
        return 'Github'

    def createInstance(self):
        return CcNetworkMetric()
