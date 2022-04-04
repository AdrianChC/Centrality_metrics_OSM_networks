"""
Model exported as python.
Name : 02 Cleaning byLayer
Group : Github
With QGIS : 31616
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterBoolean
import processing


class CleaningBylayer(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('Layer', 'Network Layer', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('CleanLayer', 'Clean Layer', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # v.clean
        alg_params = {
            '-b': False,
            '-c': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'input': parameters['Layer'],
            'threshold': '',
            'tool': [0,6],
            'type': [0,1,2,3,4,5,6],
            'error': QgsProcessing.TEMPORARY_OUTPUT,
            'output': parameters['CleanLayer']
        }
        outputs['Vclean'] = processing.run('grass7:v.clean', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CleanLayer'] = outputs['Vclean']['output']
        return results

    def name(self):
        return '02 Cleaning byLayer'

    def displayName(self):
        return '02 Cleaning byLayer'

    def group(self):
        return 'Github'

    def groupId(self):
        return 'Github'

    def createInstance(self):
        return CleaningBylayer()
