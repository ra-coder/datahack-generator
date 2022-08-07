use python3.10

# build
datahack-generator> docker compose build

# create database

    docker compose up generate    

=> таблицы в формате паркет будут в вольюме output 
(feel fry to modify docker-compose)

# test cases
Для запуска тесткейса надо выполнить команду вида 

    docker compose up test_0_a 

Для звпуска всех тестов


    docker compose up all_tests 

---
# TODO преза
#    * овервью архитектуры
#    * детали реализации генераторов
#    * плюсы что круто получилось
#       * ленивость
#       * спарк
#       * docker
#    * лайв демо на тесткейсах


---
# out of scope
## Как поднять спарк

    docker compose -f docker-compose.spark.yml -p spark up

после чего спарк дроступен тут 

    http://localhost:8080/


