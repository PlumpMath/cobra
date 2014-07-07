# -*- coding: utf-8 -*- 

from settings       import *
from collections    import deque
from random         import randrange

from helpers                        import GenLabelText, LoadObject

from panda3d.core     import Point2, Point3

class Snake( object ):
    def __init__( self, loader, camera, start_body=[(-7, 1), (-8, 1), (-9, 1)], start_vector=POS_X ):
        object.__init__( self )
        self.loader         = loader
        self.camera         = camera

        self.start_body     = deque()
        for segment in start_body:
            point = Point2( segment[X], segment[Y] )
            self.start_body.append( point )
        self.body           = deque()
        self.start_vector   = start_vector
        self.Reset()
        # self.alive          = True
        self.init_len       = len( self.start_body )

    def Reset( self ):
        self.dot            = self.GenDot()
        self.alive = True
        self.vector = self.start_vector
        for segment in self.start_body:
            brick = self.loader.loadModel( PLANE )
            brick.reparentTo( self.camera )
            brick.show()
            texture = self.loader.loadTexture( PATH_TO_SPRITES + BRICK_SPRITE )
            brick.setTexture( texture, 1 )
            brick.setPos( Point3( segment.getX(), SPRITE_POS, segment.getY() ) )
            self.body.appendleft( brick )
        print len(self.body)




    def CheckState( self ):
        head = self.body[0]
        if self.body.count( head ) > 1: 
            self.alive = False 
        elif head.getX() < -MAX_X or head.getX() > MAX_X: 
            self.alive = False 
        elif head.getY < -MAX_Y or head.getY() > MAX_Y: 
            self.alive = False 

    def MoveForward( self ):
        head = self.body[0]
        next = Point2( head.getX() + self.vector[X], head.getY() + self.vector[Y] )
        self.body.appendleft( next )
        if head == self.dot:
            self.dot = self.GenDot()
        if next != self.dot:
            self.body.pop( )

    def turn ( self, direction ):
        scal_prod   = self.vector[X] * direction[X] + self.vector[Y] * direction[Y]
        if scal_prod == 0:
            self.vector = direction

    def GenDot( self ):
        while True:
            dot    = LoadObject("brick", Point2( randrange( - MAX_X, MAX_X ), randrange( -MAX_Y, MAX_Y ) ))
            if dot not in self.body:
                return dot

    def get_score( self ):
        return len( self.body ) - self.init_len
