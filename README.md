# GIST Identity validation
As part of the cnp team, we manage multiple services for our clients, one of them are the Identity validation tickets.

Everytime a glober tries to login to the work profile on a new mobile device, we need to establish a videoconference with them in order to validate their identity.

If the glober doesn't answer, we must close the tickets in two platforms: Invgate and google admin.

## Motivation
As the work is repetitive, an opportunity to automate it was considered, in order to optimize time management and be able to do focus on more important tasks while the script is running.

## What does the script do?
Basically the script closes the tickets in both platforms, helped by selenium, an automated open-source tool which help us interact with the browser(in this case google chrome).

Once logged in, the script saves a list with all of the emails of the Identity validation tickets that the user has assigned.
After that, it executes a series of steps that are iterated for each ticket:

### Invgate
-Open the ticket
-Charge the time(5 min)
-Update the ticket status("Glober no respondió")
-Close the ticket

### Google admin
-Open a new tab
-Log into the platform
-looks for pending devices
-Based on the file which contains the mails, delete each user from the platform

## Installation


