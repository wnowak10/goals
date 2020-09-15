_goals_completer() {
 	local cur prev opts
 	COMPREPLY=()
 	cur="${COMP_WORDS[COMP_CWORD]}"
 	prev="${COMP_WORDS[COMP_CWORD-1]}"
 	
 	opts="add edit" 	
 	opts2=$(python3 /Users/willnowak/goals/goals.py return_goal_list)

	if [[ ${COMP_CWORD} -eq 1 ]] ; then
 		COMPREPLY=( $(compgen -W "${opts}" ${cur}) )
 		return 0
	fi

	case "${prev}" in
		'edit')
	if [[ ${COMP_CWORD} -eq 2 ]] ; then
 		COMPREPLY=( $(compgen -W "${opts2}" ${cur}) )
 		return 0
	fi

	esac
}
complete -F _goals_completer goals
