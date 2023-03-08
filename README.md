# DNA Center backup policy enforcement tool

As of release 2.3.5, DNA Center has the ability to do regular scheduled updates (daily, weekly or custom) but no way of setting a policy that determines how many backups are kept. This means that Operations teams must periodically check and manually delete old backups before storage runs out on the target.

This tool can be deployed in a Docker environment (any machine that runs the Docker engine) in order to enforce a backup policy for DNA Center.
