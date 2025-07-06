## Projeto Integrador - Tractomaq

#### Alunos
- Bruno Schramm Vendruscolo - 2221100004; 
- Luiz Gustavo Piuco Bazzotti - 20230001490; 
- Wendell Luis Neris - 2311100035.

### Projeto integrador das matérias de Banco de Dados I, Engenharia de Software I e Programação II. 
O objetivo da atividade é educacional, portanto o sistema será projetado acompanhando as aulas teóricas, de forma a impulsionar o aprendizado dos componentes curriculares envolvidos. O projeto se desenvolve com base na empresa Tractomaq de forma que o comunicador com a empresa, João Carvalho, participa apenas na produção relativa à Engenharia de Software, porém o projeto é realizado pelos outros integrantes exceto ele mesmo.  

#### Modelo Conceitual
![Imagem do diagrama ER do modelo conceitual do projeto](/documentos/Conceitual.png "Modelo conceitual - Tractomaq")

#### Modelo Lógico
![Imagem do diagrama do modelo lógico do projeto](/documentos/Logico.png "Modelo lógico - Tractomaq")

### Instruções - comandos para rodar a aplicação
Os arquivos referentes à prototipação podem ser econtrados na pasta "documentos".

1. Ativação do frontend
```
npm install
npm run dev
```

2. Ativação do backend
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
fastapi dev main.py
```
