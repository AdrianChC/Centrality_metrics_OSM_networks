"""
Model exported as python.
Name : 04 Network Metrics
Group : Github
With QGIS : 31616
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
import processing


class NetworkMetrics(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('CorrectedNetwork', 'Corrected Network', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Cd', 'Cd', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # v.net.centrality
        alg_params = {
            '-a': True,
            '-g': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'arc_backward_column': '',
            'arc_column': '',
            'betweenness': '',
            'cats': '',
            'closeness': '',
            'degree': 'degree',
            'eigenvector': '',
            'error': 0.1,
            'input': parameters['CorrectedNetwork'],
            'iterations': 1000,
            'node_column': '',
            'where': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Vnetcentrality'] = processing.run('grass7:v.net.centrality', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculadora Cd
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Cd',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': '\"degree\"/ minimum(\"degree\")',
            'INPUT': outputs['Vnetcentrality']['output'],
            'OUTPUT': parameters['Cd']
        }
        outputs['CalculadoraCd'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Cd'] = outputs['CalculadoraCd']['OUTPUT']
        return results

    def name(self):
        return '04 Network Metrics'

    def displayName(self):
        return '04 Network Metrics'

    def group(self):
        return 'Github'

    def groupId(self):
        return 'Github'

    def createInstance(self):
        return NetworkMetrics()
