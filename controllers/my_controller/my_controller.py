from controller import Robot

bot = Robot()

timestep = 64

# Getting devices
cam = bot.getDevice('camera')
fl = bot.getDevice('fl_wheel_joint')
fr = bot.getDevice('fr_wheel_joint')
rl = bot.getDevice('rl_wheel_joint')
rr = bot.getDevice('rr_wheel_joint')

# Initializations
cam.enable(timestep)
fl.setPosition(float('inf'))
fr.setPosition(float('inf'))
rr.setPosition(float('inf'))
rl.setPosition(float('inf'))

fl.setVelocity(0.3)
fr.setVelocity(0.3)
rr.setVelocity(0.3)
rl.setVelocity(0.3)

x_average = 0

# Main loop
while bot.step(timestep) != -1:

    # Image data
    img = cam.getImage()
    image_width = cam.getWidth()
    image_height = cam.getHeight()

    # Processing image
    x_yellow = []

    for x in range(image_width):
        for y in range(image_height):
            red_val = cam.imageGetRed(img, image_width, x, y)
            green_val = cam.imageGetGreen(img, image_width, x, y)
            blue_val = cam.imageGetBlue(img, image_width, x, y)
            print(red_val, green_val, blue_val)
            if red_val > 190 and green_val > 180 and blue_val > 90:
                x_yellow.append(x)

    # Finding average of yellow pixels
    if x_yellow:
        x_total = sum(x_yellow)
        x_average = x_total / len(x_yellow)

    # Rotating steering angle so that yellow lane remains in the center
        x_center = image_width / 2

        if x_average < x_center:  # Max pixels are on the left, take a left turn
            fl.setVelocity(3)
            rl.setVelocity(3)
            fr.setVelocity(0.3)
            rr.setVelocity(0.3)
        elif x_average > x_center:  # Max pixels are on the right, take a right turn
            fr.setVelocity(3)
            rr.setVelocity(3)
            fl.setVelocity(0.3)
            rl.setVelocity(0.3)
    else:
        fr.setVelocity(0.3)
        rr.setVelocity(0.3)
        fl.setVelocity(0.3)
        rl.setVelocity(0.3)
