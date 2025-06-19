"use strict";

figma.showUI(__html__, { width: 300, height: 400 });

figma.ui.onmessage = msg => {
  if (msg.type === 'count-elements') {
    // Get all nodes in the current page
    const allNodes = figma.currentPage.selection;
    
    // Prepare data to send back to UI
    const elements = allNodes.map(node => {
      return {
        id: node.id,
        type: node.type,
        name: node.name,
        visible: node.visible,
        children : node.children.length,
      };
    });
    
    // Send the data back to the UI
    if (node.type == "RECTANGLE" || node.type == "ELLIPSE" || node.type == "POLYGON") {
        
        elementInfo.width = Math.round(node.width);
        elementInfo.height = Math.round(node.height);
        elementInfor.x = Math.round(node.x);
        elementInfo.y = Math.round(node.y);
        if (node.fills) elementInfo.fillCount = node.fills.length;
        if (node.strokes) elementInfo.strokeCount = node.strokes.length;

    
    }

    if (node.type == "TEXT") 
    {

        elementInfo.characters = node.characters;
        elementInfo.fontSize = node.fontSize;
        elementInfo.fontName = node.fontName;

    }

    if (node.type == "FRAME" || node.type == "GROUP") 
    {
        elementInfo.childCount = node.children ? node.children.length : 0;
    }

    return elementInfo;
    
    } else if (msg.type === 'cancel') {
    figma.closePlugin();
  }
}