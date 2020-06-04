# docker-registry-to-registry-sync

A fork from docker-registry-to-registry-sync

## Goal
- Sync registries based on image_id stored in the source registry
- Have a watcher container that will watch the local registry changes periodically

## Usage

### Configuration

Create a `config.yml` file. Example:

```yaml
source_registry:
  url: https://docker.example.com
  username: some_user
  password: some_password

destination_registry:
  url: http://127.0.0.1:5000

repeat_every: 120

```

The meaning of the settings:

* `source-registry`: The registry to sync from
* `destination-registry`: The registry to sync to
* `repeat_every`: repeat the sync operation every x seconds
  
When the images are synced, the registry part of the tag is replaced, e.g.
in the example above the tag `docker.example.com/company/super-project` is
re-tagged as `127.0.0.1:5000/company/super-project` and pushed to `127.0.0.1:5000`.

### Passwords as environment variables

You can specify the registry passwords using`config.yml` file.

### Running via docker

1. Create `deploy_config.yml` and put your configuration in it, in the same directory

2. Run `setup-cotnainer.sh` script
