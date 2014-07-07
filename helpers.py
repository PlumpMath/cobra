# -*- coding: utf-8 -*- 

from settings                   import *

from panda3d.core               import Point2, Point3
from panda3d.core               import TextNode

from direct.gui.OnscreenText    import OnscreenText

def GenLabelText( text, i, left=True ):
    label           = OnscreenText( text=text )
    label["fg"]     = ( 0.148, 0.176, 0.105, 1 )
    label["align"]  = TextNode.ALeft
    label["scale"]  = 0.06
    label["font"]   = loader.loadFont( 'data/fonts/DejaVuSansMono.ttf' )
    if left:    label["pos"] = ( -1.3, 0.95-0.06*i )
    else:       label["pos"] = ( 0.95, 0.95-0.06*i )
    return label

def LoadObject( tex=None, pos=Point2( 0, 0 ), depth=SPRITE_POS, scale=1, transparency=True ):
    obj = loader.loadModel( "data/models/plane" )
    obj.reparentTo( camera )
    obj.setPos( Point3( pos.getX(), depth, pos.getY() ) )
    obj.setScale( scale )
    obj.setBin( "unsorted", 0 )
    obj.setDepthTest( False )
    if transparency: 
        obj.setTransparency( 1 )
    if tex:
        tex = loader.loadTexture( "data/sprites/"+tex+".png" ) 
        obj.setTexture( tex, 1 )
    return obj
