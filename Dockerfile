FROM python:3.8
USER root
RUN mkdir/app
copy . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENV AIRFLOW_HOME='app/airflow'
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True
RUN airflow db init 
RUN airflow users create -e mahammadrafishaik222@gmail.com -f maha -l rafi -p admin -r admin -u admin
RUN chmod 777 start.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT ["bin/sh"]
CMD ["start.sh"]