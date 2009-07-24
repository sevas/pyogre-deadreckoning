# This code is in the Public Domain
#

import ogre.renderer.OGRE as ogre

# We don't use the verisons but it's nice to set them up...
ogre.OgreVersion = ogre.GetOgreVersion()
ogre.OgreVersionString = ogre.OgreVersion[0] + ogre.OgreVersion[1] + ogre.OgreVersion[2]
ogre.PythonOgreVersion = ogre.GetPythonOgreVersion()

from ogre.renderer.OGRE.sf_OIS import * 
           
    
