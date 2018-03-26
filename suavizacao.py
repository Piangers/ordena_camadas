# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Suavizacao
                                 A QGIS plugin
 ferramenta
                              -------------------
        begin                : 2018-03-07
        git sha              : $Format:%H$
        copyright            : (C) 2018 by piangers
        email                : cesar_piangers@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import math
from qgis.core import QgsMapLayerRegistry,QgsMapLayer
from qgis.core import QGis, QgsVectorLayer, QgsGeometry,QgsLayerTreeGroup,QgsLayerTreeLayer,QgsProject
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QAction
#include <qgslayertreeviewdefaultactions.h>
#include <qgslayertreegroup.h>
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from suavizacao_dialog import SuavizacaoDialog
import os.path
from qgis.gui import QgsMessageBar
import collections

class Suavizacao:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        
        # Declare instance attributes
        self.actions = []
        self.menu = u'&Organiza_camada'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Organiza_camada')
        self.toolbar.setObjectName(u'Organiza_camada')

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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = SuavizacaoDialog()

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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Suavizacao/c.png'
        self.add_action(
            icon_path,
            text=u'Organiza_camada',
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&Organiza_camada', action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


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
