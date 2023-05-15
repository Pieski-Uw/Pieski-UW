#check if there are four arguments
if [ $# -ne 5 ]
then
    echo "Usage: $0 <db_host> <db_port> <db_user> <db_password> <db_name>"
    exit 1
fi

#generate postgresql file with arguments
cat > pieskiUW/secrets/postgresql.py << EOF
SECRETS = {
   "HOST": "$1",
   "PORT": $2,
   "USER": "$3",
   "PASSWORD": "$4",
   "NAME": "$5",
}
