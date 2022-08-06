FROM node:12-alpine \
    RUN npm install -g yarn \
    RUN yarn install \
    WORKDIR /app \
    COPY . . \
    EXPOSE 8080 \
    CMD ["npm", "start"]

RUN apt-get update \
 && apt-get install -y locales \
 && dpkg-reconfigure -f noninteractive locales \
 && locale-gen C.UTF-8 \
 && /usr/sbin/update-locale LANG=C.UTF-8 \
 && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
 && locale-gen \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \

# Users with other locales should set this in their derivative image
ENV LANG en_US.UTF-8 \
ENV LANGUAGE en_US:en \
ENV LC_ALL en_US.UTF-8 \

RUN apt-get update \
 && apt-get install -y curl \
    python3 python3-setuptools \
 && ln -s /usr/bin/python3 /usr/bin/python \
 && easy_install3 pip py4j \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# http://blog.stuart.axelbrooke.com/python-3-on-spark-return-of-the-pythonhashseed
ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# this installs packages mentioned in requirements-pip.txt
ADD requirements-pip.txt .
RUN pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements-pip.txt

# SPARK
services:
   app:
     image: apache/spark-py	# spark-py is a docker image
     command: /usr/bin/python3 app.py	# app.py is the entrypoint
     ports:
       - "8080:8080"			# expose port 8080 on host
     volumes:
       - ./data:/data			# mount volume from host to container
       - ./logs:/logs			# mount volume from host to container
     environment:
       - SPARK_MASTER_HOST=spark-master	# set spark-master as spark master
       - SPARK_MASTER_PORT=7077		# set spark-master port
       - SPARK_WORKER_CORES=1		# set number of cores for spark worker
       - SPARK_WORKER_MEMORY=1g		# set memory for spark worker
       - SPARK_WORKER_INSTANCES=1		# set number of spark worker instances
       - SPARK_DRIVER_MEMORY=1g		# set memory for spark driver
       - SPARK_DRIVER_CORES=1		# set number of cores for spark driver
       - SPARK_EXECUTOR_MEMORY=1g		# set memory for spark executor
       - SPARK_EXECUTOR_CORES=1		# set number of cores for spark executor
       - SPARK_EXECUTOR_INSTANCES=1		# set number of spark executor instances
       - SPARK_DAEMON_MEMORY=1g		# set memory for spark daemon
       - SPARK_DAEMON_CORES=1		# set number of cores for spark daemon
       - SPARK_DAEMON_INSTANCES=1		# set number of spark daemon instances
       - SPARK_DIST_CLASSPATH=$(hadoop classpath)	# set classpath for spark
       - SPARK_HOME=/usr/local/spark		# set spark home
       - SPARK_CONF_DIR=/usr/local/spark/conf	# set spark conf dir
       - SPARK_LOG_DIR=/logs			#


CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]