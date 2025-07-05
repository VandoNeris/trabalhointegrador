## Projeto Integrador - Tractomaq

#### Alunos
- Bruno Schramm Vendruscolo - 2221100004; 
- Luiz Gustavo Piuco Bazzotti - 20230001490; 
- Wendell Luis Neris - 2311100035.

### Projeto integrador das matérias de Banco de Dados I, Engenharia de Software I e Programação II. 
O objetivo da atividade é educacional, portanto o sistema será projetado acompanhando as aulas teóricas, de forma a impulsionar o aprendizado dos componentes curriculares envolvidos. O projeto se desenvolve com base na empresa Tractomaq de forma que o comunicador com a empresa, João Carvalho, participa apenas na produção relativa à Engenharia de Software, porém o projeto é realizado pelos outros integrantes exceto ele mesmo.  

#### Modelo Conceitual
![Imagem do diagrama ER do modelo conceitual do projeto](/documentos/Conceptual%20Model.png "Modelo conceitual - Tractomaq")

#### Modelo Lógico
![Imagem do diagrama do modelo lógico do projeto](/documentos/Logical%20Model.png "Modelo lógico - Tractomaq")

### Instruções - comandos para rodar a aplicação
Os arquivos referentes à prototipação podem ser econtrados na pasta "documentos".

1. Ativação do ambiente virtual
```
python -m venv venv
venv\Scripts\activate
```

2. Rodar o servidor e carregar no app
```
fastapi dev main.py
```
