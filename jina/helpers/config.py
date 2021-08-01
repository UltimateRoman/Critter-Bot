from jina import Executor, Document, DocumentArray, requests
import os
import itertools

top_k = 1
max_docs = 100


class SimpleIndexer(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._docs = DocumentArray()
        self.top_k = top_k
        if os.path.exists(self.save_path):
            self._docs = DocumentArray.load(self.save_path)
        else:
            self._docs = DocumentArray()

    @property
    def save_path(self):
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        return os.path.join(self.workspace, "dogs.json")

    def close(self):
        self._docs.save(self.save_path)

    @requests(on="/index")
    def index(self, docs: "DocumentArray", **kwargs):
        self._docs.extend(docs)
        return docs

    @requests(on="/search")
    def search(self, docs, **kwargs):
        darr = self._docs
        return darr



def docs_generator(input_file, num_docs=max_docs):

    with open(input_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in itertools.islice(reader, num_docs):
            input_data = row['breed']
            doc = Document(text=input_data)
            doc.tags = row[0]
            yield doc
                
                    


def check_workspace(dir_name, should_exist=False):
    if should_exist:
        if not os.path.isdir(dir_name):
            print(
                f"The directory {dir_name} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)

    if not should_exist:
        if os.path.isdir(dir_name):
            print("Deleting the old workspace..")
            shutil.rmtree(dir_name)


