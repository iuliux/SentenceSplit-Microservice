# SentenceSplit-Microservice

API for sentence splitting.

## Usage
- The API accepts only `POST` requests, expects `JSON` input and produces `JSON` output.
- Make sure to also provide some value for `x-access-token` header, otherwise the access will be forbidden (ask the administrators for a valid token).
- The request body should contain `text` key with some string to split, then the response body will be a list of corresponding sentences.

## Deploy and Update
In order to deploy a new environment (let's call it `env`), make appropriate changes in `zappa_settings.json` (i.e. add and fill respectively a new section called `"env"`) and then run
```shell
zappa deploy env
```
In order to push changes to an already existing and deployed environment (let it be `env` again) simply run
```shell
zappa update env
```
After updating the environment make sure to check that the tests still pass by running
```shell
zappa manage env "test core"
```
