# AlphaVantage simple calculations

In order to run this you need to define your AlphaVantage API key in the environment variables as `API_KEY`.

To unpack and run:
~~~
cd build
docker build -t deliveryquiz .
docker run --env-file=FILE deliveryquiz --env-file=FILE
~~~
`FILE` should contain the `API_KEY` entry

## Future work
Testing :see_no_evil: