
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


# Time Clicker 

Time Clicker is a clicker where you gain Time Units in order to advance the Timeline to discord new age

## Features

- **Time Units Generation**: Click to generate Time Units and advance through different eras.
- **Buildings**: Purchase and upgrade various buildings to increase your Time Units per second (TPS).
- **Upgrades**: Unlock and buy upgrades to boost the efficiency of your buildings.
- **Timeline**: Progress through the timeline by reaching specific milestones and unlocking new eras.
- **Human Skills**: Improve human skills such as strength, agility, and intelligence to gain various in-game benefits.
- **Cables**: Interact with blue and red cables to gain temporary boosts or face challenges.
- **Auto-Save**: The game automatically saves your progress at regular intervals.
- **AFK Time Units**: Earn Time Units even when you are away from the game.
- **Responsive UI**: The game interface adapts to different screen sizes and resolutions.

## Controls and Key Bindings

- **Mouse Click**: Click on the hourglass to generate Time Units.
- **Mouse Wheel**: Scroll through the list of available buildings and upgrades.
- **F11**: Toggle fullscreen mode.
- **Ctrl + F1**: Reset the game.
- **Escape**: Exit the game.
- **Space**: Click the hourglass to generate Time Units (alternative to mouse click).
- **Mouse Click on Buildings**: Purchase buildings to increase TPS.
- **Mouse Click on Upgrades**: Buy upgrades to boost building efficiency.
- **Mouse Click on Timeline**: Advance the timeline to unlock new eras.
- **Mouse Click on Human Skills**: Improve human skills to gain various benefits.
- **Mouse Click on Cables**: Interact with blue and red cables for temporary boosts or challenges.
## How to Start

To start the game, run the executable file:

```sh
./TimeClicker.exe
```
## Bug History  

This section documents previously encountered issues and their resolutions to track development progress and improvements.  

- **Saving Data**  
  - Issue: Player data was not always saving correctly, leading to potential progress loss.  
  - Fix: Implemented a more reliable saving mechanism to ensure all game states are properly stored.  

- **Retrieving Time Units from AFK**  
  - Issue: The game was not correctly awarding time units after a player returned from AFK, causing inaccurate offline progression.  
  - Fix: Adjusted the time tracking system to ensure the correct amount of time units is granted based on the player's AFK duration.  

- **Resetting Blue Cable Boost**  
  - Issue: The blue cable boost did not reset properly under certain conditions, leading to unintended stacking or persistent effects.  
  - Fix: The boost now correctly resets after its designated duration

- **TPS Accuracy (High Priority)**  
  - Issue: The game’s ticks per second (TPS) did not align properly with real-world time, affecting time-dependent mechanics.  
  - Fix: Adjusted frame-based calculations so that each frame contributes the correct amount of time, ensuring accurate pacing and game mechanics.  


## Authors

- [Xalri](https://www.github.com/Xalri)
- [Rex14_0](https://www.github.com/Rex140-hub)
- [Akisuko](https://www.github.com/Krinoceros)


## Support

For support:
- email xalri@xalri.ovh
- add **xalri** on [discord](https://discord.com)
- add **rex14_0** on [discord](https://discord.com)
- add **akisuk0** on [discord](https://discord.com)

