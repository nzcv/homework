docker run -d \
  --name mysql57 \
  -e MYSQL_ROOT_PASSWORD=1234 \
  -p 3306:3306 \
  mysql:8.0