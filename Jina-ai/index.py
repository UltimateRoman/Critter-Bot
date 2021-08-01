from jina import Flow, DocumentArray, Document
from helpers.config import SimpleIndexer, is_workspace
from jina.types.document.generators import from_csv
import csv, os


encoder = 'jinahub://TransformerTorchEncoder'
model = "sentence-transformers/msmarco-distilbert-base-v3"
port = 12345
max_docs = 1000
indexer = SimpleIndexer
workspace_dir = os.path.join(os.path.abspath('workspace'))
datafile = os.path.abspath(os.path.dirname(__file__) + "/./dogs.csv")


da = DocumentArray()
with open('./dogs.csv', 'r') as data:
    for line in csv.DictReader(data):
        d = Document(line)
        da.append(d)
        

def index(num_docs=max_docs):
    flow = (
        Flow()
        .add(
            uses=encoder,
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=indexer, workspace=workspace_dir, name="indexer", dump_path=workspace_dir, override_with={"index_file_name": "index.json"})
    )

    with flow:
        flow.post(
            on="/index",
            inputs=docs_generator(input_file=datafile, num_docs=num_docs),
            request_size=64,
            read_mode="r",
        )


def query_restful():
    flow = (
        Flow()
        .add(
            uses=encoder,
            pretrained_model_name_or_path=model,
            name="encoder",
            max_length=50,
        )
        .add(uses=indexer, workspace=workspace_dir, name="indexer", dump_path=workspace_dir, override_with={"index_file_name": "index.json"})
    )

    with flow:
        flow.protocol = "http"
        flow.port_expose = port
        flow.block()


def indexer():
    is_workspace(dir_name=workspace_dir, should_exist=False)
    index(num_docs=max_docs)

def query():
    is_workspace(dir_name=workspace_dir, should_exist=True)
    query_restful()


