from urllib.parse import urlparse

import os
import yaml
import docker
from connector import RegistryConnector


def strip_scheme(url):
    parsed_url = urlparse(url)
    scheme = "%s://" % parsed_url.scheme
    return parsed_url.geturl().replace(scheme, '', 1)


def load_config():
    with open('config.yml') as f:
        return yaml.load(f)


def push_changes(repository, tag):
    print(repository, tag)

if __name__ == '__main__':

    config = load_config()


    src_registry_meta = {}
    dst_registry_meta = {}

    try:
        src_client = RegistryConnector(config, "source_registry")
        src_registry_meta = src_client.fetch_registry_meta()
        src_registry_digest =  src_registry_meta.keys()
        #
        dst_client = RegistryConnector(config, "destination_registry")
        dst_registry_meta = dst_client.fetch_registry_meta()
        dst_registry_digest = dst_registry_meta.keys()
        # Check if something new is added to source registry
        new_diff = src_registry_digest - dst_registry_digest

        if len(new_diff) == 0:
            print("Repositories are synced")
            exit(0)

        # Login registries
        docker_client = docker.from_env()
        print("Logging in source registry")
        docker_client.login(
                registry= src_client.registry_url, 
                username= src_client.username,
                password= src_client.password
        )

        print("Logging in destination registry")
        docker_client.login(
                registry= dst_client.registry_url, 
                username= dst_client.username,
                password= dst_client.password
        )


        for diff in new_diff:
            diff_tag = src_registry_meta[diff]
            src_new_tag = "{}/{}".format(strip_scheme(src_client.registry_url), diff_tag)
            dst_new_tag = "{}/{}".format(strip_scheme(dst_client.registry_url), diff_tag)

            print("New update in {}".format(src_new_tag))
                    
            # pull the image
            docker_client.images.pull(src_new_tag)
            # get the image and update its tag  
            src_image = docker_client.images.get(name=src_new_tag)
            src_image.tag(dst_new_tag)

            # PUSHH
            print("Pushing {}".format(dst_new_tag))
            docker_client.images.push(dst_new_tag)

    except IOError as io:
        print ("ERROR:" + str(io))
        exit(-1)

    exit(0)
