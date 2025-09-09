# ha-person-notify

This integration has the goal to provides a more user/person centric way of notifying users. 

## Features
- Auto create notify groups for each person, that is tied back to the user.
- Action sendmessagedynamic: Send a message to the user, that was responsible for triggering an automation.

## Setup
Add `personnotify:` to your configuration.yaml, then restart Home Assistant

## How to use
### Groups
Go to Helpers, your notify groups should be listed there.
<img width="1368" height="419" alt="image" src="https://github.com/user-attachments/assets/0403f463-f539-4f94-9bdd-f5a70713b07c" />

### Action
Add the `sendmessagedynamic` action to your automation. \
The action should figure out, where to send the message.
<img width="1357" height="510" alt="image" src="https://github.com/user-attachments/assets/5dd69d4b-62ef-4e85-87ed-6b3e48ac2d58" />

## TODOs
- Create group on person creation (Groups for users are only created at startup, so if you create a new user you have to restart the instance.)
- Implement deleting group of deleted person enitity
- Implement Config_flow

## Implementation
Notify group entites have the user_id attribute in the data of the config_entry. \
This ties the entity back to the exact person entity, even if the person entity is renamed.

The sendmessagedynamic action relies my ha-whodid package. \
If a message isnt sent, the fault is probably there. \
https://github.com/Tabisch/ha-whodid

## MISC
If most or all your notify are services you can try this integration. \
https://github.com/Tabisch/ha-notify-conversion \
This let's you "convert" notify services to notify entities.
