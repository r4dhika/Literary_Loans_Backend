FROM python:3.9

RUN pip install virtualenv

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY ./ /code/

RUN python3 -m venv myenv
RUN /bin/bash -c "source myenv/bin/activate"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN python3 ./literaryLoans/manage.py makemigrations
RUN python3 ./literaryLoans/manage.py migrate

EXPOSE 8000

CMD ["python3", "./literaryLoans/manage.py", "runserver", "0.0.0.0:8000"]
