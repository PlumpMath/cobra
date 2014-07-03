# -*- coding: utf-8 -*- 

import sys
import snake

from panda3d.core                   import Point2

from direct.showbase.ShowBase       import ShowBase
from direct.task.Task               import Task
from direct.gui.DirectGui           import DirectFrame

from settings                       import *
from helpers                        import genLabelText, loadObject
from collections                    import deque

class World( ShowBase ):
    def __init__ ( self ):
        ShowBase.__init__( self )

        self.disableMouse( )

        self.background     = loadObject( "background", scale=9000, depth=200, transparency=False )
        self.gameboard      = loadObject( "background", scale=39.5, depth=100, transparency=False )
        self.escape_text    = genLabelText( "ESC  : Quit", 0 )
        self.pause_text     = genLabelText( "SPACE: Pause", 1)
        self.reset()
        self.score          = genLabelText( "SCORE: %s" % self.snake.get_score( ), 0, left=False )
        self.some_frame     = DirectFrame( frameColor=(0, 1, 0, 1), frameSize=(-1, 1, -1, 1), pos=(0,0,0) )
        self.some_frame.reparentTo( self.render2d )
        self.some_frame.hide()
        
        self.accept( "escape",      sys.exit )
        self.accept( "enter",       self.reset )
        self.accept( "arrow_up",    self.snake.turn, [ POS_Y ] )
        self.accept( "arrow_down",  self.snake.turn, [ NEG_Y ] )
        self.accept( "arrow_left",  self.snake.turn, [ NEG_X ] )
        self.accept( "arrow_right", self.snake.turn, [ POS_X ] )
        self.accept( "space",       self.tooggle_pause )

        self.game_task      = taskMgr.add( self.game_loop, "GameLoop" )
        self.game_task.last = 0
        self.period         = 0.15
        self.pause          = False


    def game_loop( self, task ):
        dt = task.time - task.last
        if not self.snake.alive: 
            for brick in self.bricks:
                brick.removeNode()
            self.dot.removeNode()
            return task.cont
        if self.pause:
            return task.cont
        elif dt >= self.period:
            task.last = task.time
            self.snake.move_forward( )
            self.snake.check_state( )
            self.update_snake( )
            self.update_dot( )
            self.update_score( )
            return task.cont
        else:
            return task.cont


    def draw_snake( self ):
        for point in self.snake.body:
            brick = loadObject( "brick", pos=Point2( point[ X ], point[ Y ] ) )
            self.bricks.append( brick )

    def reset( self ):
        self.snake          = snake.Snake( body=[ (-7, 1), (-8, 1), (-9, 1) ], dot=(-7, 1) )
        self.snake.gen_dot( )
        self.bricks         = deque( )
        self.make_dot( )
        self.draw_snake( )


    # def remove_snake( self ):
    #     for brick in self.bricks:
    #         brick.removeNode()
        
    #     if self.dot:
    #         self.dot.removeNode()

    # def restart( self ):
    #     self.remove_snake()
    #     self.reset()

    def update_snake( self ):
        try:
            for i in xrange( len( self.snake.body ) ):
                point   = self.snake.body[ i ]
                brick   = self.bricks[ i ]
                brick.setPos( point[ X ], SPRITE_POS, point[ Y ] )
        except IndexError:
            new_head    = self.dot
            self.make_dot( )
            self.bricks.appendleft( new_head )

    def make_dot( self ):
        self.dot = loadObject( "brick", pos=Point2( self.snake.dot[ X ], self.snake.dot[ Y ] ) ) 

    def update_dot( self ):
        x, y = self.dot.getX( ), self.dot.getZ( )
        if ( x, y ) != self.snake.dot:
            self.dot.setPos( self.snake.dot[ X ], SPRITE_POS, self.snake.dot[ Y ] )

    def update_score( self ):
        self.score.setText( "Score: %s" % self.snake.get_score( ) )

    def tooggle_pause( self ):
        if self.pause:  self.pause = False
        else:           self.pause = True

w   = World( )
w.run( )
