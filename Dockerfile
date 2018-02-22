FROM python:3

ADD cryptocalculator.py /
ADD cryptofetcher.py /

RUN pip3 install pandas
RUN pip3 install alpha_vantage
RUN mkdir outputs

CMD [ "python3", "./cryptocalculator.py" ]