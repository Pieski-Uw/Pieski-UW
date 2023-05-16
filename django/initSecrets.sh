#/bin/bash
if [ $# -ne 5 ]
then
    echo "Usage: $0 <db_host> <db_port> <db_user> <db_password> <db_name>"
    exit 1
fi


cat > django/pieskiUW/secrets/postgresql.py << EOF
# pylint: disable=line-too-long
SECRETS = {
    "HOST": "$1",
    "PORT": $2,
    "USER": "$3",
    "PASSWORD": "$4",
    "NAME": "$5",
}

# pytlint: enable=line-too-long
