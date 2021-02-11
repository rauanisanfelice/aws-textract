import boto3
import datetime
import json
import logging

from pdf2image import convert_from_path
from trp import Document
from os import walk

FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
TEXTRACT = boto3.client('textract')


def ListFiles(path: str, prefix: str) -> list:
    f = []
    AddPrefix = lambda prefix, elem: { 'fullPathName': f'./{prefix}/{elem}', 'fullName': elem, 'name': elem.split(".")[0], 'extent': elem.split(".")[1] }
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        f1 = list(map(AddPrefix, [prefix] * len(f), f))
        break
    return f1


def PDFToPNG(file: str):

    try:
        pages = convert_from_path(
            file['fullPathName'],
            dpi=500, fmt="png",
            output_folder="./img/",
            output_file=file['name']
        )
        return pages

    except Exception as error:
        logging.error(error)
        return None


def ImageToBytes(listFiles):
    """
    Function tha get file and return ByteArry

    param:
        * path: of file

    return:
        * Bytearray
        * None: Error
    """
    try:
        f = []
        logging.info("Convertendo File para ByteArry")
        for image in listFiles:
            logging.info(f"{image.filename}")
            with open(image.filename, 'rb') as document:
                f.append(bytearray(document.read()))
        return f 

    except Exception as error:
        logging.error(error)
        return None


def AnalyzeDocument(byteImages):
    """
    Function that analyze a image and return one document
    
    params:
        * image bytearry
    
    return:
        * None: erro in read image
        * Document: result of image
    """

    f = []
    logging.info('Analizando arquivo(s)')
    for byteImage in byteImages:
        response = TEXTRACT.analyze_document(
            Document={
                'Bytes': byteImage
            },
            FeatureTypes=["FORMS"])
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            f.append(Document(response))

        else:
            logging.info('Erro ao Analizar arquivo')
            return None
    
    return f


def ReadResultDocument(docs, file):
    
    blocks = []
    count = 0
    for doc in docs:
        for page in doc.pages:
            EntityTypes = []
            count +=1
            for field in page.form.fields:

                keyValue = field.key.text.encode("ISO-8859-1").decode("ISO-8859-1")
                keyConfidence = round(field.key.confidence,2)

                valueValue = field.key.text.encode("ISO-8859-1").decode("ISO-8859-1") if field.value is not None else None
                valueConfidence = round(field.value.confidence,2) if field.value is not None else None
                
                EntityTypes.append({
                    'key': {
                        'value': keyValue, 
                        'confidence': keyConfidence,
                    },
                    'value': {
                        'value': valueValue,
                        'confidence': valueConfidence,
                    }
                })
                
            blocks.append({
                'page': f'Page: {count}',
                'EntityTypes': EntityTypes
            })

    result = {
        'file': file['name'],
        'pages': len(docs),
        'blocks': blocks
    }

    result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=4)
    with open(f"./json/{file['name']}.json", 'w', encoding="utf-8") as json_file:
        json_file.write(result)


def main():

    logging.info("Inicio")
    start_time = datetime.datetime.now()

    logging.info("Listando arquivos...")
    listFiles = ListFiles("./pdf/", "pdf")

    if not listFiles:
        logging.critical("Nenhum arquivo localizado.")
        return


    for file in listFiles:
        logging.info(f"{file['name']}")
        logging.info("Convertendo PDF para PNG")
        images = PDFToPNG(file)
        byteImages = ImageToBytes(images)
        docs = AnalyzeDocument(byteImages)

        logging.info(f"Salvando resultados")
        if docs is not None:
            ReadResultDocument(docs, file)
    
    logging.info("Time: " + str(datetime.datetime.now()  - start_time))
    

if __name__ == "__main__":
    main()

