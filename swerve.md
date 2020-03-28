# Swerve drive test kit

* Use left analog stick to control the direction of the robot
* Press one of the four digital buttons (square, triangle, circle, and cross)
  with left analog stick to move individual motors separately.
  This is primarily used to align four tires into the same direction.
  When aligned, press the option button to lock the initial location
  
## Design Notes
* Reading the current tacho meter seems to only work with the layer 0 motors,
  so in the current design, all the layer 0 motors control directions, and
  all the layer 1 motors control the forward motions.