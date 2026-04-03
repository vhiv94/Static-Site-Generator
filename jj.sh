jj commit -m $1
jj bookmark create $2 -r @-
jj bookmark track $2
jj git push