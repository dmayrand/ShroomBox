import picamera
from time import sleep

camera = picamera.PiCamera()
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 70
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'night'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 90
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.resolution = "HD"


for i in range(12):
  print('capturing image #' + str(i+1))
  camera.capture('img' + str(i) + '.jpg')
  sleep(5)
