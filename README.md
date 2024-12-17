# RAGInvest

To setup all the airflow components run:<br>

<code>
echo -e "AIRFLOW_UID=$(id -u)" > .env
<br>AIRFLOW_UID=50000
<br>docker-compose up airflow-init
<br>docker-compose up
<br>docker ps
</code>
<br>
Search for localhost:8080<br>
Username: airflow<br>
Password: airflow<br>