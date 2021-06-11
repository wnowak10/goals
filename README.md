
## Installation

I assume that both `python3` and `/usr/local/bin` are in your path.

    cd
    git clone https://github.com/wnowak10/goals.git
    ln -s ./goals/goals.py /usr/local/bin/goals

Additionally, you need to have a `goals.json` file in your user's home directory. 

--

Then call AppleScript App from iCal [events.](https://softron.zendesk.com/hc/en-us/articles/360000261674-HOW-TO-Trigger-an-AppleScript-at-specific-date-and-time):


## TO DO:

Additionally, to get tab autocomplete, add the following lines to ~/.zshrc.

```
autoload bashcompinit
bashcompinit
source ~/goals/goalcomplete.bash
```

To add aliases fir zsh users. 

unalias g # Git alias
alias ge="goals edit"
alias gt="goals todos"