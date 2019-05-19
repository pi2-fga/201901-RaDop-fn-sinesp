# FN-SINESP

[![Build Status](https://travis-ci.org/radar-pi/fn-sinesp.svg?branch=develop)](https://travis-ci.org/radar-pi/fn-sinesp)
[![Maintainability](https://api.codeclimate.com/v1/badges/4616194d10b706ff4bf8/maintainability)](https://codeclimate.com/github/radar-pi/fn-sinesp/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4616194d10b706ff4bf8/test_coverage)](https://codeclimate.com/github/radar-pi/fn-sinesp/test_coverage)

A **Função SINESP** é a função responsável por avaliar junto com o banco de dados do SINESP a situação de cada veículo. Dado o modelo de dados enviado o serviço irá pesquisar junto ao dados do SINESP informação cadastrais, assim como situação, restrições, ano, modelo, cor e outras informações sobre o veículo indicado.

## Parâmetros

Os parâmetros da função fn-sinesp seguem o modelo de dados do pacote (_package_) de mensagens da arquitetura do sistema do radar. Eles consistem em um objeto JSON com o seguinte formato:

- **id**: Um UUID para identificar unicamente aquele pacote (tipo `string`).

- **type**: Qual o tipo da chamada de função, para que a função possa identificar se o pacote que ele recebeu é do seu domínio. Para a função SINESP só serão aceitos pacotes com a chave `sinesp-call` (tipo `string`).

- **payload**: Será um outro objeto JSON com o conteúdo da mensagem (tipo `dict`).

    - **plate**: A placa do carro a ser analisado no banco de dados do SINESP (tipo `string`).

- **time**: O dia e horário em que essa mensagem foi enviado no formato RFC3339, ou seja, `YYYY-MM-DDTHH:MM:SSZ` (tipo `string`).

__Exemplo__:

```json
{
  "id": "44b314eb-b67d-4b4f-b744-4772c5954601",
  "type": "sinesp-call",
  "payload": {
    "plate": "AAA1234"
  },
  "time": "2019-04-27T10:14:35Z"
}
```

## Tecnologias Utilizadas

- Plataforma OpenFaaS
    - _Self-Hosted_ Function as a Service
- Python 3
- JSON
- [Sinesp Client](https://github.com/victor-torres/sinesp-client)

## Ambiente de Desenvolvimento

Recomendado o uso de OpenFaaS local em Docker Swarm.

O guia para criar o ambiente local está disponível [na seção de _Deployment_ da documentação do OpenFaaS](http://docs.openfaas.com/deployment/docker-swarm/).

Editor de texto de preferência.

## Ambiente de Teste Local

Recomendados a utilização de um ambiente virtual criado pelo módulo `virtualenvwrapper`.
Existe um sítio virtual com instruções em inglês para a instalação que pode ser acessado [aqui](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Mas você pode também seguir o roteiro abaixo para a instalação do ambiente:

```shell
python3 -m pip install -U pip # Faz a atualização do pip
python3 -m pip install virtualenvwrapper # Caso queira instalar apenas para o usuário use a opt --user
```

Agora configure o seu shell para utilizar o virtualenvwrapper, adicionando essas duas linhas ao arquivo de inicialização do seu shell (`.bashrc`, `.profile`, etc.)

```shell
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Caso queira adicionar um local específico de projeto basta adicionar uma terceira linha com o seguinte `export`:

```shell
export PROJECT_HOME=/path/to/project
```

Execute o arquivo de inicialização do shell para que as mudanças surtam efeito, por exemplo:

```shell
source ~/.bashrc
```

Agora crie um ambiente virtual com o seguinte comando (colocando o nome que deseja para o ambiente), neste exemplo usarei o nome composta:

```shell
mkvirtualenv fn-sinesp
```

Para utilizá-lo:

```shell
workon fn-sinesp
pip install -r compiler/requirements.txt # Irá instalar todas as dependências usadas no projeto
```

**OBS**: Caso o sua variável de ambiente *PROJECT_HOME* esteja _setada_ ao executar o `workon` você será levado para o diretório lá configurado.

Para outras configurações e documentação adicional acesse a página do [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

## Deploy Local para Desenvolvimento

Para deploy da função, basta seguir o roteiro abaixo:

```shell
$ faas build -f fn-sinesp.yml
$ faas deploy -f fn-sinesp.yml
```

Para utilizá-lo, teste pela interface web no endereço definido, chamar pela CLI, ou por requisição HTTP:

FaaS CLI:

```shell
$ echo $'{\n  "id": "44b314eb-b67d-4b4f-b744-4772c5954601",\n  "type": "sinesp-call",\n  "payload": {\n    "plate": "AAA1234"\n  },\n  "time": "2019-04-27T10:14:35Z"\n}' | faas-cli invoke fn-sinesp

HTTP-Request:

```shell
$ curl -d $'{\n  "id": "44b314eb-b67d-4b4f-b744-4772c5954601",\n  "type": "sinesp-call",\n  "payload": {\n    "plate": "AAA1234"\n  },\n  "time": "2019-04-27T10:14:35Z"\n}' -X POST http://127.0.0.1:8080/function/fn-sinesp
```

Exemplo de saída:

```shell
{"status_code": 200, "response": {"return_code": "0", "return_message": "Sem erros.", "status_code": "0", "status_message": "Sem restrição", "chassis": "14117", "model": "GM/CHEVROLET D20 CUSTOM", "brand": "GM/CHEVROLET D20 CUSTOM", "color": "Azul", "year": "1988", "model_year": "1988", "plate": "AAA1234", "date": "06/05/2019 às 22:33:14", "city": "CURITIBA", "state": "PR"}}
```

## Execução do Ambiente de Testes

Para executar os testes do fn-alpr siga o roteiro descrito abaixo:

Primeiro assegure-se de que tem todas as dependências necessárias para executar o projeto.

```shell
$ pip install -r fn-sinesp/requirements.txt
# Ou caso não esteja trabalhando com uma virtualenv
$ python3 -m pip install -r fn-sinesp/requirements.txt
```

**OBS**: Caso queria instalar apenas para o usuário e não no sistema use a opt `--user` ao final do comando pip.

Agora que todas as dependências estão instaladas basta rodar o comando do pytest para verificar se o código está de acordo com o teste.

```shell
$ pytest fn-sinesp/ # Executa os testes no pytest
$ py.test --cov=fn-alpr fn-sinesp/ # Executa os testes e avalia a cobertura estática de código
$ py.test --cov=fn-alpr --cov-report html fn-sinesp/ # Faz o mesmo papel que o comando anterior, além de gerar uma pasta htmlcov/ com uma página relatório da cobertura
$ flake8 fn-sinesp/* # Executa o PEP8 linter nos arquivos python
```

Durante o `pytest` e o `py.test`, o terminal lhe apresentará um _output_ com o relatório dos testes e a cobertura de testes da aplicação. Para outras configuraões e documentação complementar acesse o sítio virtual do provedor do [pytest](https://docs.pytest.org/en/latest/) e do [coverage](https://pytest-cov.readthedocs.io/en/latest/).

Durante o `flake8`, o terminal lhe apresentará um relatório com os erros e _warnings_ do guia de estilo PEP8 do python, para demais configurações e documentações você pode acessar o sítio do [flake8](http://flake8.pycqa.org/en/latest/index.html) ou visualizar o estilo do [PEP8](https://www.python.org/dev/peps/pep-0008/).