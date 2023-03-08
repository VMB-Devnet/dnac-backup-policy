# DNA Center backup policy enforcement tool

As of release 2.3.5, DNA Center has the ability to do regular scheduled updates (daily, weekly or custom) but no way of setting a policy that determines how many backups are kept. This means that Operations teams must periodically check and manually delete old backups before storage runs out on the target.

This tool can be deployed in a Docker environment (any machine that runs the Docker engine) in order to enforce a backup policy for DNA Center. The script runs daily at 2AM and retrieves the list of backups from DNA Center. Based on the retention policy set by the user, it deletes backups starting with the oldest ones until the number of backups in DNA Center matches the retention policy.

## Deployment guide

### Requirements

In order to use the tool you will need the following:

1) Computer or VM running any OS that supports the Docker engine (compatible OS's can be found here - https://docs.docker.com/engine/install/)
2) The comupter or VM must be able to reach DNA Center 
3) A DNA Center user with administrator access (not recommended) or with read/write access to Platform APIs and System Management (recommended - a custom profile with these permissions can be created in DNA Center under "Users & Roles" > "Role Based Access Control")
4) (Optional) A Webex personal access token (not recommended) or a BOT access token (recommended). This will allow the tool to send confirmation messages whenever it successfully runs.

### Configuration and deployment

1) Download the tool or clone the repository into a folder on the machine the runs the Docker engine.
2) Before deploying the tool you must edit the ".env" file with the values specific to your setup. Each value is explained below:

**DNA_CENTER_BASE_URL** - this is the IP or FQDN of the DNA Center that the tool will connect to.  
**DNA_CENTER_USERNAME** - this is the username that the tool will use to connect to DNA Center.  
**DNA_CENTER_PASSWORD** - this is the password that the tool will use to connect to DNA Center.  
**WEBEX_NOTIFICATION_ENABLED** - can be "True" or "False" (no quotes). If "True" the tool will send a Webex Teams message with each successfull run to the person set in the "WEBEX_RECIPIENT" variable. If "False" the tool will not send a Webex Teams notifications.  
**WEBEX_TOKEN** - the Webex API token to use. Can be either personal or BOT token (BOT token is recommended) - see https://developer.webex.com/docs/bots for details on how to obtain the token.  
**WEBEX_RECIPIENT** - email of person to whom the confirmation message will be sent when the tool successfully runs. The email must be associated with a Webex Teams user.  
**RETENTION_POLICY** - number of DNA Center backups to keep. If set to 0, the tool will delete all backups.  

Below is the ".env" file supplied in the project:

DNA_CENTER_BASE_URL=YOUR_DNAC_FQDN_HERE  
DNA_CENTER_USERNAME=YOUR_DNAC_USER_HERE  
DNA_CENTER_PASSWORD=YOUR_DNAC_PASSWORD_HERE  
WEBEX_NOTIFICATION_ENABLED=True  
WEBEX_TOKEN=YOUR_WEBEX_TOKEN_HERE  
WEBEX_RECIPIENT=WEBEX_TEAMS_EMAIL  
RETENTION_POLICY=2  

This is an example of a completed ".env" file for customer Ficticious Industries Inc (their domain is "fi.com" in this example). This customer has Webex Teams notifications disabled and has a policy that keeps the 5 newest backups:

DNA_CENTER_BASE_URL=dnac.fi.com  
DNA_CENTER_USERNAME=administrator  
DNA_CENTER_PASSWORD=super_secret  
WEBEX_NOTIFICATION_ENABLED=False  
WEBEX_TOKEN=YOUR_WEBEX_TOKEN_HERE  
WEBEX_RECIPIENT=EMAIL_OF_RECIPIENT  
RETENTION_POLICY=5  

This is an example of a completed ".env" file for customer NHS Narnia (their domain is "narnia.nhs.uk" in this example). This customer has Webex Teams notifications enabled and has a policy that keeps the 2 newest backups:

DNA_CENTER_BASE_URL=dnac.narnia.nhs.uk  
DNA_CENTER_USERNAME=administrator  
DNA_CENTER_PASSWORD=super_secret  
WEBEX_NOTIFICATION_ENABLED=True  
WEBEX_TOKEN=ZDA4YWI2NjYtNzc3Ni00YmRlLTldasdsakdkhlasddkYTAyZjJhOTYtNjJk_PF84_cca99e60-7e42-4fa8-ab73-90635eb378a6  
WEBEX_RECIPIENT=the.it.guy@narnia.nhs.net  
RETENTION_POLICY=2  

Note: the token in the example above is only an example.

3) From the directory where the "docker-compose.yml" file and the "app" folder are located, run the following commands:

**docker-compose build --no-cache**  
**docker-compose up -d**  

### Checking the deployment

To check that the container has been deployed correctly run:

**docker ps**  

You should then see a list of all running containers and there should be an entry that looks like this:

CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                                                                NAMES
9219d84b7f51   dnac-backup-policy:latest   "crond -f"               43 seconds ago   Up 42 seconds                                                                                                        DNAC-backup-policy

Note: The "CONTAINER ID", "CREATED" and "STATUS" fields will be different. A successfull deployment should show similar values for "CREATED" and "STATUS".
