# SentenceSplit-Microservice

[![CircleCI](https://circleci.com/gh/BeagleInc/SentenceSplit-Microservice.svg?style=svg&circle-token=7c554f769570976c81e7d7523c0dd0059d9e27d1)](https://circleci.com/gh/BeagleInc/SentenceSplit-Microservice)

API for sentence splitting.

Current working environments:
- `dev`: https://kyhk5y2ub3.execute-api.us-west-2.amazonaws.com/dev

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
