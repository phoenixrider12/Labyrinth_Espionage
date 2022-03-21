# Labyrinth_Espionage

The GitHub Repository of Team Espionage for Labyrinth'22, a ROS-based event conducted by IIT Varanasi, where we bagged first position

## Run the simulation

- Clone this repository in the `src` folder of your catkin workspace.
- Inside your workspace folder, run `catkin build`.
- Open a terminal and run the following command to start the simulation:
  ```
  roslaunch labyrinth labyrinth_husky_arena.launch
  ```
  - Open a new terminal and run the following command:
  ```
  roslaunch labyrinth_navigation labyrinth_gmapping.launch
  ```
  - Open a new terminal and run the following command:
  ```
  rosrun spy spy.py
  ```
  - Open a new terminal and run the following command:
  ```
  rosrun labyrinth_navigation moveyourbody.py
  ```

### Team
<table>
	<td align="center">
     <a href="https://github.com/phoenixrider12">
    <img src="https://avatars.githubusercontent.com/u/76533398?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Aryaman Gupta</b></sub></a><br />
	</td>
 <td align="center">
     <a href="https://github.com/san2130">
    <img src="https://avatars.githubusercontent.com/u/88130555?v=4" width="100px;" alt=""/><br /><sub><b>Sandeepan Ghosh</b></sub></a><br />
    </td>
 <td align="center">
     <a href="https://github.com/Ankur-Agrawal-ece20">
    <img src="https://avatars.githubusercontent.com/u/78701055?v=4" width="100px;" alt=""/><br /><sub><b>Ankur Agrawal</b></sub></a><br />
    </td>


</table>
