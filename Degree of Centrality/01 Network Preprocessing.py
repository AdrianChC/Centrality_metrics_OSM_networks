"""
Model exported as python.
Name : 01 Network Preprocessing
Group : Github
With QGIS : 31616
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterExpression
from qgis.core import QgsProcessingParameterFolderDestination
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsCoordinateReferenceSystem
import processing


class NetworkPreprocessing(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('OpenNetworkLayer', 'Open Network Layer', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterExpression('TargetCRS', 'Target_CRS', optional=True, parentLayerParameterName='', defaultValue='QgsCoordinateReferenceSystem(EPSG:32718)'))
        self.addParameter(QgsProcessingParameterFolderDestination('BylayersFolder', 'byLayers Folder', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Extraer Oneway T
        alg_params = {
            'EXPRESSION': '\"oneway\"=t',
            'INPUT': parameters['OpenNetworkLayer'],
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtraerOnewayT'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Invertir dirección de línea
        alg_params = {
            'INPUT': outputs['ExtraerOnewayT']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['InvertirDireccinDeLnea'] = processing.run('native:reverselinedirection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Oneway correction
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['ExtraerOnewayT']['FAIL_OUTPUT'],outputs['InvertirDireccinDeLnea']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['OnewayCorrection'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Filter roads
        # Filtering roads that are just pedestrian, internal or service.
That is code < 5140
        alg_params = {
            'EXPRESSION': 'code < 5140',
            'INPUT': outputs['OnewayCorrection']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FilterRoads'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Dividir capa vectorial
        alg_params = {
            'FIELD': 'layer',
            'FILE_TYPE': 0,
            'INPUT': outputs['FilterRoads']['OUTPUT'],
            'OUTPUT': parameters['BylayersFolder']
        }
        outputs['DividirCapaVectorial'] = processing.run('native:splitvectorlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BylayersFolder'] = outputs['DividirCapaVectorial']['OUTPUT']
        return results

    def name(self):
        return '01 Network Preprocessing'

    def displayName(self):
        return '01 Network Preprocessing'

    def group(self):
        return 'Github'

    def groupId(self):
        return 'Github'

    def createInstance(self):
        return NetworkPreprocessing()
