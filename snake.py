# -*- coding: utf-8 -*- 

from settings       import *
from collections    import deque
from random         import randrange

from panda3d.core     import Point2

class Snake( object ):
    def __init__( self, body=[ (0, 0), (1, 0), (2, 0)], vector=NEG_X ):
        object.__init__( self )
        self.body           = deque()

        for segment in body:
            point = Point2( segment[0], segment[1] )
            self.body.appendleft( point )
        self.vector         = vector
        self.dot            = self.GenDot()
        self.alive          = True
        self.init_len       = len( self.body )
        head = self.body[0]

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
            dot    = Point2( randrange( - MAX_X, MAX_X ), randrange( -MAX_Y, MAX_Y ) )
            if dot not in self.body:
                return dot

    def get_score( self ):
        return len( self.body ) - self.init_len
