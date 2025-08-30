# ha-person-notify

Creates Notify group entities for each user. \
Groups for users are only created at startup, so if you create a new user you have to restart the instance.

Entites have the user_id attribute in the data of the config_entry. \
This ties the entity back to the exact person entity, even if the person entity is renamed.

If most or all your notify are services you can try this integration. \
https://github.com/Tabisch/ha-notify-conversion \
This let's you "convert" notify services to notify entities.