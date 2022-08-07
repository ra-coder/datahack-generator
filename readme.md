use python3.10

# Build

    docker compose build

# Create database

    docker compose up generate    

=> таблицы в формате паркет будут в вольюме output 
(feel fry to modify docker-compose)

# Test cases
Для запуска тесткейса надо выполнить команду вида 

    docker compose up test_0_a 

Для звпуска всех тестов

    docker compose up all_tests 

---
# out of scope
## Как поднять спарк

    docker compose -f docker-compose.spark.yml -p spark up

после чего спарк дроступен тут 

    http://localhost:8080/


