# DNA Center backup policy enforcement tool

As of release 2.3.5, DNA Center has the ability to do regular scheduled updates (daily, weekly or custom) but no way of setting a policy that determines how many backups are kept. This means that Operations teams must periodically check and manually delete old backups before storage runs out on the target.

This tool can be deployed in a Docker environment (any machine that runs the Docker engine) in order to enforce a backup policy for DNA Center. The script runs daily at 2AM and retrieves the list of backups from DNA Center. Based on the retention policy set by the user, it deletes backups starting with the oldest ones until the number of backups in DNA Center matches the retention policy.

## Deployment guide

### Requirements

In order to use the tool you will need the following:

1) Computer or VM running any OS that supports the Docker engine (compatible OS's can be found here - https://docs.docker.com/engine/install/)
2) The comupter or VM must be able to reach DNA Center 

### Configuration

Before deploying the tool you must edit the ".env" file with the values specific to your setup. Each value is explained below:

DNA_CENTER_BASE_URL - this is the IP or FQDN of the DNA Center that the tool will connect to.
DNA_CENTER_USERNAME - this is the username that the tool will use to connect to DNA Center.
DNA_CENTER_PASSWORD - this is the password that the tool will use to connect to DNA Center.
WEBEX_NOTIFICATION_ENABLED - can be "True" or "False" (no quotes). If "True" the tool will send a Webex Teams message with each successfull run to the person set in the "WEBEX_RECIPIENT" variable. If "False" the tool will not send Webex Teams notifications.
WEBEX_TOKEN - the Webex API token to use. Can be either personal or BOT token (BOT token is recommended) - see https://developer.webex.com/docs/bots for details on how to obtain the token.
WEBEX_RECIPIENT - email of person to whom the confirmation message will be sent when the tool successfully runs.
RETENTION_POLICY - number of DNA Center backups to keep. If set to 0, the tool will delete all backups.

Below is the ".env" file supplied in the project:

DNA_CENTER_BASE_URL=YOUR_DNAC_FQDN_HERE
DNA_CENTER_USERNAME=YOUR_DNAC_USER_HERE
DNA_CENTER_PASSWORD=YOUR_DNAC_PASSWORD_HERE
WEBEX_NOTIFICATION_ENABLED=True
WEBEX_TOKEN=YOUR_WEBEX_TOKEN_HERE
WEBEX_RECIPIENT=EMAIL_OF_RECIPIENT
RETENTION_POLICY=2

An example of a completed ".env" file for customer Ficticious Industries Inc (their domain is "fi.com" in this example):

DNA_CENTER_BASE_URL=dnac.fi.com
DNA_CENTER_USERNAME=administrator
DNA_CENTER_PASSWORD=super_secret
WEBEX_NOTIFICATION_ENABLED=True
WEBEX_TOKEN=YOUR_WEBEX_TOKEN_HERE
WEBEX_RECIPIENT=EMAIL_OF_RECIPIENT
RETENTION_POLICY=2
