#!/bin/bash

mongod -f mongo-fork.conf

sleep 5

mongo admin --eval 'db.createUser({
user:"admin",
pwd:"admin",
roles:[{
role:"userAdminAnyDatabase",
db:"admin"
}]
});
db.auth("admin", "admin");'

mongo xtest --eval 'db.createUser({
user:"xtest",
pwd:"xtest@2018",
roles:[{
role:"readWrite",
db:"xtest"
}]
});
db.auth("xtest", "xtest@2018");'

sleep 5 && echo "Initialized!"