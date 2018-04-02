# -*- coding: utf-8 -*-

import math
from qgis.core import QgsMapLayerRegistry,QgsMapLayer
from qgis.core import QGis, QgsVectorLayer, QgsGeometry,QgsLayerTreeGroup,QgsLayerTreeLayer,QgsProject
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QAction
from PyQt4.QtCore import *
import resources_rc
import os.path
from qgis.gui import QgsMessageBar
import collections

class Suavizacao:

    def __init__(self, iface):
        
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/Suavizacao/c.png'
        
        
        self.action = QAction (QIcon (icon_path),'Organiza Camadas', pai)
        self.action.setObjectName ('Organiza Camadas')
        self.action.setStatusTip('status_tip')
        self.action.setWhatsThis('whats_this')
        QObject.connect (self.action, SIGNAL ("triggered ()"), self.run)

        # Adicionar o botão da barra de ferramentas e item de menu 
        self.iface.addToolBarIcon (self.action) 
        self.iface.addPluginToMenu ("&Organiza Camadas", self.action)



    def unload(self):
        
        self.iface.removePluginMenu(u'&Organiza Camadas', self.action)
        self.iface.removeToolBarIcon(self.action)
        # remove the toolbar

    def run(self):
        grupo = self.testGrupoAtivo()
        if(grupo):
            if(self.testMaisCamadaGrupo(grupo)):   
                pass
            if(self.organizaGrupo(grupo)):
                pass

    def testGrupoAtivo(self):
            for camadas in self.iface.layerTreeView().selectedNodes():
                if(not len(self.iface.layerTreeView().selectedNodes()) == 1):
                    self.iface.messageBar().pushMessage(u'Selecione somente um grupo.', level=QgsMessageBar.INFO, duration=5)
                    return False
                elif(not camadas.__class__.__name__ == "QgsLayerTreeGroup"):
                    self.iface.messageBar().pushMessage(u'Selecione um tipo grupo.', level=QgsMessageBar.INFO, duration=5)
                    return False
                else:
                    return self.iface.layerTreeView().selectedNodes()[0] 
        
    def testMaisCamadaGrupo(self, grupo):
        if not len(grupo.findLayers()) > 1:
            self.iface.messageBar().pushMessage(u'O Grupo deve conter mais de uma camada', level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            pass

    def organizaGrupo(self,grupo):
        filhos = grupo.children()
        organizado = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        
        for filho in filhos:
            if(filho.__class__.__name__ == "QgsLayerTreeLayer"):
                layer = filho.layer()
                if(layer.type() == QgsMapLayer.VectorLayer):
                    if(layer.featureCount() == 0):
                        organizado[2].append(filho)
                    elif(layer.geometryType() == QGis.Point):
                        organizado[3].append(filho)
                    elif(layer.geometryType() == QGis.Line):
                        organizado[4].append(filho)
                    elif(layer.geometryType() == QGis.Polygon):
                        organizado[5].append(filho)
                elif(layer.type() == QgsMapLayer.RasterLayer):
                    organizado[6].append(filho)
                else:
                        organizado[7].append(filho)
            else:
                organizado[1].append(filho)
        
        for indice in organizado.keys():
            lista = organizado[indice]

        listaOrganizada = organizado[1]
        self.bubble_sort_group(listaOrganizada)
        
        for grupoOriginal in listaOrganizada:
            grupoCopia = grupoOriginal.clone()
            grupo.addChildNode(grupoCopia)
            grupo.removeChildNode(grupoOriginal)
            self.organizaGrupo(grupoCopia)

        for i in range(2,8):
            listaOrganizada = organizado[i]
            self.bubble_sort_layer(listaOrganizada)
            
            for layerOriginal in listaOrganizada:
                layerCopia = layerOriginal.clone()
                grupo.addChildNode(layerCopia)
                grupo.removeChildNode(layerOriginal)
        
    def bubble_sort_layer(self, seq):
        changed = True
        while changed:
            changed = False
            for i in range(len(seq) - 1):
                if seq[i].layer().name() > seq[i+1].layer().name():
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    changed = True

    def bubble_sort_group(self, seq):
        changed = True
        while changed:
            changed = False
            for i in range(len(seq) - 1):
                if seq[i].name() > seq[i+1].name():
                    seq[i], seq[i+1] = seq[i+1], seq[i]
                    changed = True
