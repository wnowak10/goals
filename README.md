
## Installation

I assume that both `python3` and `/usr/local/bin` are in your path.

    cd # https://www.youtube.com/watch?v=IKJqecxswCA (To home directory)
    git clone https://github.com/wnowak10/goals.git 
    ln -s ./goals/goals.py /usr/local/bin/goals # Symlink to create goals command.

Additionally, you need to have a `goals.json` file in your user's home directory. 

## Usage

Use `goals help` for docstrings.

A "session", unless otherwise noted, represents a focused 25 minute block of time.

    Usage:

        # Print out current goals:
            $ goals

        # Add new goals:
            $ goals add <GOAL>

        # Mark goal progress
            $ goals edit <GOAL>

        # See notes on a goal
            $ goals details <GOAL>

        # Set timer to focus on a goal
            $ goals timer <TIME>

## Use AppleScript to run on a schedule. (Hacky)

Then call AppleScript App from iCal [events.](https://softron.zendesk.com/hc/en-us/articles/360000261674-HOW-TO-Trigger-an-AppleScript-at-specific-date-and-time):


## To enable tab autocomplete, add the following lines to ~/.zshrc:

```
autoload bashcompinit
bashcompinit
source ~/goals/goalcomplete.bash
```

## To add aliases for zsh users:

	unalias g # Git alias
	alias ge="goals edit"
	alias gt="goals todos"
