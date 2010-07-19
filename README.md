Description
-----------

Dead-reckoning is a technique to estimate the position of moving objects based on previous positions.
This is useful for moving entities in networked applications, like multiplayer games.

This demo simulates moving entities by generating new positions randomly, one per second. It then builds a spline to smoothly move the entity until we get a new position update.

This implementation may not fit every situation where dead-reckoning is needed.
However, it might be useful to someone.

Dependencies
------------

Requires a working version of python-ogre (http://www.pythonogre.com/). If the official demos work, you should be fine.

Licence
-------

WTFPL. 
See COPYING file for details.