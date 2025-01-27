# RAGInvest

<h4>To setup all the airflow components run:</h4>

<code>echo -e "AIRFLOW_UID=$(id -u)" > .env
<br>AIRFLOW_UID=50000
<br>docker-compose up airflow-init
<br>docker-compose up
<br>docker ps
</code>
<br>
Search for localhost:8080<br>
Username: < Enter Your username ><br>
Password: < Enter Your password ><br>

<h4>To setup PostGreSQL DB</h4>
<code>docker run --name postgresQL -p 5432:5432 -e POSTGRES_PASSWORD=< enter your password> -d postgres
</code>
<ul>
<li>-p for port</li>
<li>-d for detached</li>
<li>-e for Environment Variables</li>
<li>postgresQL - Name of Container (Can be of your choice)</li>
<li>postgres - Image (Do not change)</li>
<li>username: postgres</li>
<li>database: postgres</li>
<li>host: localhost</li>
</ul>
<!-- <br> -->
<!-- <br> -->
Connect using DBeaver or PgAdmin
<br>
To run logstash's docker compose file<br>
<code>cd logstash/<br>
docker compose up<br>
docker ps
</code><br>
You should have 3 new containers running:
<ol>
<li>Kibana</li>
<li>ElasticSearch</li>
<li>Logstash</li>
</ol>