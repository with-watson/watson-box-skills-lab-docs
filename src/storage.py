from boxsdk import OAuth2, Client


class Storage(object):
    """Represents an instace of storage, in this case is a way of accessing
       Box"""
    def __init__(self, config: dict, request_body: dict) -> 'Storage':
        self.config = config
        self.request_body = request_body
        self.file_data = self._make_file_data()  # {name: "", id: 0000}
        self.download_path = request_body['source']['name']
        self.download_token = request_body['token']['read']['access_token']
        self.upload_token = request_body['token']['write']['access_token']

    def _make_file_data(self) -> dict:
        """Get the file data, useful for upload
        """
        data = {}
        data['name'] = self.request_body['source']['name']
        data['id'] = self.request_body['source']['id']
        return data

    def connect(self, token: str) -> 'Client':
        """Connect to box using a bearer token

            Args:
                token: The bearer token to use for this connection
        """
        if self.config['storage'] == 'box':
            auth = OAuth2(None, None, access_token=token)
            return Client(auth)
        else:
            raise Exception('Invalid Storage Option: ' +
                            self.config['storage'])

    def download_file(self) -> str:
        """Download the file that this should be working on to local
           container
        """
        if self.config['storage'] == 'box':
            with open(self.download_path, 'wb') as storage_file:
                storage = self.connect(self.download_token)
                storage.file(file_id=self.file_data['id']).download_to(
                    storage_file)
        else:
            raise Exception("Error downloading file: is the storage set up correctly?")
        return self.download_path

    def update_file(self, metadata: dict, file_id: int = None) -> None:
        """Update the metadata of a file

           Args:
                metadata: A dict with the correct format od a bsk card.
                file_id: The id of the file to append the metadata to, if none
                    assumed to be the calling function
        """
        storage = self.connect(self.upload_token)
        if file_id is None:
            file_id = self.file_data['id']
        try:
            storage.file(file_id=file_id).metadata(
                template='boxSkillsCards').create(metadata)
        except Exception as e:
            print(e)
            try:
                storage.file(file_id=file_id).metadata(
                    template='boxSkillsCards').get()
                file_metadata = storage.file(
                    file_id=file_id).metadata(template='boxSkillsCards')
                update = file_metadata.start_update()
                for item in metadata:
                    update.add('/' + item, metadata[item])
                file_metadata.update(update)
            except Exception as e:
                print(str(e))
                print('Something went wrong on metadata creation...')
