"""
Model exported as python.
Name : 03 Cross Layer Correction
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


class CrossLayerCorrection(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('Layer0', 'Clean Layer n', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('MergeCleanLayer', 'Merge Clean Layers', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('CrossLayer', 'Cross Layer', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # v.net
        alg_params = {
            '-c': False,
            '-s': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'arc_type': [0,1],
            'file': '',
            'input': parameters['MergeCleanLayer'],
            'operation': 0,
            'points': None,
            'threshold': 50,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Vnet'] = processing.run('grass7:v.net', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 0.5,
            'END_CAP_STYLE': 0,
            'INPUT': outputs['Vnet']['output'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Diferencia
        alg_params = {
            'INPUT': parameters['Layer0'],
            'OVERLAY': outputs['Buffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferencia'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Multiparte a monoparte
        alg_params = {
            'INPUT': outputs['Diferencia']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultiparteAMonoparte'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Ajustar geometrías a capa
        alg_params = {
            'BEHAVIOR': 0,
            'INPUT': outputs['MultiparteAMonoparte']['OUTPUT'],
            'REFERENCE_LAYER': outputs['Vnet']['output'],
            'TOLERANCE': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AjustarGeometrasACapa'] = processing.run('native:snapgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Quitar campo FID
        alg_params = {
            'COLUMN': ['fid'],
            'INPUT': outputs['AjustarGeometrasACapa']['OUTPUT'],
            'OUTPUT': parameters['CrossLayer']
        }
        outputs['QuitarCampoFid'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CrossLayer'] = outputs['QuitarCampoFid']['OUTPUT']
        return results

    def name(self):
        return '03 Cross Layer Correction'

    def displayName(self):
        return '03 Cross Layer Correction'

    def group(self):
        return 'Github'

    def groupId(self):
        return 'Github'

    def shortHelpString(self):
        return """<html><body><h2>Descripción del algoritmo</h2>
<p>Not neccesary to apply to clean layer 0
This is intended for the other layers</p>
<h2>Parámetros de entrada</h2>
<h3>Clean Layer n</h3>
<p></p>
<h3>Merge Clean Layers</h3>
<p></p>
<h3>Cross Layer</h3>
<p></p>
<h3>Verbose logging</h3>
<p></p>
<h2>Salidas</h2>
<h3>Cross Layer</h3>
<p></p>
<br></body></html>"""

    def createInstance(self):
        return CrossLayerCorrection()
