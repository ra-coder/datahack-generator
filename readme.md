use python3.10


datahack-generator> docker compose build

datahack-generator> docker compose up   
[+] Running 2/2
 - Network datahack-generator_default  Created                                                                                                                         0.6s 
 - Container datahack-generator-app-1  Created                                                                                                                         0.1s
Attaching to datahack-generator-app-1
datahack-generator-app-1  | User(id=11026, name='todo_rand_str', group_id=5)
datahack-generator-app-1  | User(id=8444, name='todo_rand_str', group_id=3)
datahack-generator-app-1  | User(id=10175, name='todo_rand_str', group_id=2)
datahack-generator-app-1 exited with code 0



---
Как поднять спарк

    docker compose -f docker-compose.spark.yml -p spark up

после чего спарк дроступен тут 

    http://localhost:8080/