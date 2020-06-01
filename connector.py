from docker_registry_client import DockerRegistryClient

class RegistryConnector(DockerRegistryClient):
    def __init__(self, config, registry_key, url_key="url", username_key="username", password_key="password"):
        def get_credentials(config, registry):
            username = None if username_key not in  config[registry] else str(config[registry][username_key])
            password = None if password_key not in  config[registry] else str(config[registry][password_key])
            return username, password

        registry_url = config[registry_key][url_key]
        username, password = get_credentials(config, registry_key)

        self.username = username
        self.password = password
        self.registry_url = registry_url

        super(RegistryConnector, self).__init__(
                registry_url, 
                username=username,
                password=password
                )


    """
    will return a meta registry 
    {
        "digest_id": repository:tag
    }
    """
    def fetch_registry_meta(self):
        meta_table = {}
        repositories = self.repositories().keys()

        for r in repositories:
            r_ = {}
            # get tags + digest
            for t in self.repository(r).tags():
                meta_table[self.repository(r).manifest(t)[1]] = r + ":" + t
        return meta_table
