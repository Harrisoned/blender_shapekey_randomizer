# Blender Shapekey Randomizer

This plugin was made to mimic some procedurally generated animations  commonly found in game engines.

## Overview

The Blender Shapekey Randomizer allows you to apply randomized shapekey animations to selected meshes. This is particularly useful for creating natural, organic animations such as blinking, muscle twitches, or subtle facial movements. This plugin was made to mimic some procedurally generated animations commonly found in game engines. It's my first plugin for Blender, so use at your own risk.

## Features

- Allows users to select specific shapekeys to randomize.

- Configurable parameters per shapekey, including:

  - Minimum and maximum interval between activations.

  - Duration of the shapekey effect.

  - Transition speeds for smooth animation.

  - Min/max shapekey values for precise control.

- Shapekey panels are created dynamically, and users can remove them individually.

- Animations are automatically keyframed based on configured randomness.

- Works within Blender's frame change handler for seamless integration with animation workflows.

## Installation

- Download the `shapekey_randomizer.py` script.

- Open Blender and navigate to `Edit > Preferences > Add-ons`.

- Click `Install...`, select the downloaded script, and enable the add-on.

- The plugin will now be available in the `Object Properties` panel.

## Usage

1. Select an object (mesh) that contains shapekeys.

2. Go to the Object Properties panel and find the Shapekey Randomizer section.

3. Click Select Shapekeys to choose which shapekeys you want to randomize.

4. Adjust parameters for each selected shapekey:

    - Min/Max Interval: Controls how often the shapekey activates.

    - Duration: Determines how long the effect lasts.

    - In/Out Speed: Defines transition smoothness.

    - Min/Max Value: Controls the shapekey intensity.

5. Click Start Randomizer to begin animation automation.

6. Play your animation using the Timeline to the plugin starts to generate keyframes
     -  This is important. The whole system is frame-based, so it will only generate the keyframes during playtime.

8. Pause/Stop your animation when you are done.

9. Click Stop Randomizer to halt the effect in future playbacks.

If needed, remove individual shapekeys from the panel using the Remove button.

## Animation Patterns

- The plugin applies keyframes automatically based on randomized intervals.

- It smoothly transitions between the minimum and maximum values over the configured in/out speeds.

- Each selected shapekey operates independently, allowing for varied animation timing.

## Known Limitations

- The animation randomness is frame-dependent, meaning results may vary at different frame rates. It is sometimes inconsistent as well, but should save you some time by adding repetitive patterns for you. You can cut or copy-paste them later in the graph editor to further adjust the animations.

- Since it relies on Blender’s frame change handler, excessive use may impact performance in complex scenes.
