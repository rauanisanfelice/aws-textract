![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rauanisanfelice/aws-textract.svg)
![GitHub top language](https://img.shields.io/github/languages/top/rauanisanfelice/aws-textract.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rauanisanfelice/aws-textract.svg)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rauanisanfelice/aws-textract)
![GitHub contributors](https://img.shields.io/github/contributors/rauanisanfelice/aws-textract.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/rauanisanfelice/aws-textract.svg)

![GitHub stars](https://img.shields.io/github/stars/rauanisanfelice/aws-textract.svg?style=social)
![GitHub followers](https://img.shields.io/github/followers/rauanisanfelice.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/rauanisanfelice/aws-textract.svg?style=social)

# aws-textract

Ferramenta que lê os arquivos PDFs, realiza OCR e salva em JSON.

## Intruções

1. Virtual env;
2. Dependências;
3. Configurações AWS;
4. Executar script;

### Virtual env
```
virtualenv -p python3 env
source env/bin/activate
```

### Dependências
```
pip3 install -r requirements.txt
```

### Configurações AWS
```
sudo apt install awscli -y
aws configure
```

### Executar script
```
python main.py
```

Arquivo que foi utilizado de exemplo:

https://pt.wikipedia.org/wiki/Nota_fiscal_eletr%C3%B4nica