# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtWidgets import *
from OrganizaGrupo import resources_rc



class OrganizaGrupo:

    
    def __init__(self, iface):
       
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BGTImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        self.actions = []
        self.menu = self.tr(u'&Batch Vector Layer Saver')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BatchVectorLayerSaver')
        self.toolbar.setObjectName(u'fecha_linha')

       
    def tr(self, message):
        
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BatchVectorLayerSaver', message)
        
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
       
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
         
        icon_path = ':/plugins/OrganizaGrupo/c.png'
        self.add_action(
            icon_path,
            text=self.tr(u'OrganizaGrupo'),
            callback=self.run,
            parent=self.iface.mainWindow())    
    

        # # Adicionar o botão da barra de ferramentas e item de menu 
        # self.iface.addToolBarIcon (self.action) 

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&OrganizaGrupo'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar  
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        grupo = self.testGrupoAtivo()
        if(grupo):
            if(self.testMaisCamadaGrupo(grupo)):   
                pass
            if(self.organiza(grupo)):
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

    def organiza(self,grupo):
        filhos = grupo.children()
        organizado = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        
        for filho in filhos:
            if(filho.__class__.__name__ == "QgsLayerTreeLayer"):
                layer = filho.layer()
                if(layer.type() == QgsMapLayer.VectorLayer):
                    if(layer.featureCount() == 0):
                        organizado[2].append(filho)
                    elif(layer.geometryType() == 0):
                        organizado[3].append(filho)
                    elif(layer.geometryType() == 1):
                        organizado[4].append(filho)
                    elif(layer.geometryType() == 2):
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
            #self.organizaGrupo(grupoCopia)

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
